import os
from django.core.management.base import BaseCommand
from opensearchpy import OpenSearch
from api.models import Blog


class Command(BaseCommand):
    help = 'Sync blog data to OpenSearch index'

    def handle(self, *args, **options):
        try:
            client = OpenSearch(
                hosts=[{'host': 'opensearch', 'port': 9200}],
                http_auth=('admin', os.getenv('OPENSEARCH_INITIAL_ADMIN_PASSWORD')),
                use_ssl=True,
                verify_certs=False,
                ssl_assert_hostname=False,
                ssl_show_warn=False,
            )
            
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
                self.stdout.write(f'Created OpenSearch index: {index_name}')
            
            blogs = Blog.objects.all()
            synced_count = 0
            
            for blog in blogs:
                doc = {
                    'title': blog.title,
                    'content': blog.content,
                    'category': blog.category,
                    'created_at': blog.created_at.isoformat()
                }
                client.index(index=index_name, id=blog.pk, body=doc)
                synced_count += 1
            
            client.indices.refresh(index=index_name)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully synced {synced_count} blog entries to OpenSearch'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error syncing blogs to OpenSearch: {str(e)}')
            )
            return
