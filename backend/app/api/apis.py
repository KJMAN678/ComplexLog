import os
from typing import Optional
from ninja import NinjaAPI, Query
from opensearchpy import OpenSearch
from api.models import Blog


api = NinjaAPI()


def get_opensearch_client():
    client = OpenSearch(
        hosts=[{'host': 'opensearch', 'port': 9200}],
        http_auth=('admin', os.getenv('OPENSEARCH_INITIAL_ADMIN_PASSWORD')),
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
    return client


def ensure_blog_index():
    client = get_opensearch_client()
    index_name = 'blogs'
    
    if not client.indices.exists(index=index_name):
        mapping = {
            'mappings': {
                'properties': {
                    'title': {'type': 'text', 'analyzer': 'standard'},
                    'content': {'type': 'text', 'analyzer': 'standard'},
                    'category': {'type': 'keyword'},
                    'created_at': {'type': 'date'}
                }
            }
        }
        client.indices.create(index=index_name, body=mapping)
    
    return client, index_name


def sync_blogs_to_opensearch():
    client, index_name = ensure_blog_index()
    
    blogs = Blog.objects.all()
    for blog in blogs:
        doc = {
            'title': blog.title,
            'content': blog.content,
            'category': blog.category,
            'created_at': blog.created_at.isoformat()
        }
        client.index(index=index_name, id=blog.pk, body=doc)
    
    client.indices.refresh(index=index_name)


@api.get("/")
def index(request):
    return {"test": 1}


@api.get("/sync-blogs")
def sync_blogs(request):
    try:
        sync_blogs_to_opensearch()
        return {"status": "success", "message": "Blogs synced to OpenSearch"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@api.get("/search")
def search_blogs(request, q: str = Query(...), category: Optional[str] = Query(None)):
    try:
        client, index_name = ensure_blog_index()
        
        query_body = {
            "query": {
                "bool": {
                    "must": []
                }
            },
            "size": 20,
            "sort": [{"created_at": {"order": "desc"}}]
        }
        
        if q.strip():
            query_body["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": q,
                    "fields": ["title^2", "content"],
                    "type": "best_fields"
                }
            })
        else:
            query_body["query"] = {"match_all": {}}
        
        if category and category in ['news', 'poem']:
            if query_body["query"]["bool"]["must"]:
                query_body["query"]["bool"]["must"].append({
                    "term": {"category": category}
                })
            else:
                query_body["query"] = {
                    "bool": {
                        "must": [{"term": {"category": category}}]
                    }
                }
        
        response = client.search(index=index_name, body=query_body)
        
        results = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            results.append({
                'id': hit['_id'],
                'title': source['title'],
                'content': source['content'],
                'category': source['category'],
                'created_at': source['created_at'],
                'score': hit['_score']
            })
        
        return {
            "status": "success",
            "results": results,
            "total": response['hits']['total']['value'],
            "opensearch_logs": {
                "query": query_body,
                "response_time": response.get('took', 0),
                "total_hits": response['hits']['total']['value'],
                "max_score": response['hits']['max_score'],
                "raw_response": response
            }
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e),
            "opensearch_logs": {
                "error": str(e)
            }
        }
