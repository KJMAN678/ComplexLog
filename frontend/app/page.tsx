'use client';

import { useState } from 'react';

interface SearchResult {
  id: string;
  title: string;
  content: string;
  category: string;
  created_at: string;
  score: number;
}

interface SearchResponse {
  status: string;
  results: SearchResult[];
  total: number;
  opensearch_logs: Record<string, unknown>;
}

export default function Page() {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [opensearchLogs, setOpensearchLogs] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('検索クエリを入力してください');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const params = new URLSearchParams();
      params.append('q', query);
      if (category) {
        params.append('category', category);
      }

      const response = await fetch(`http://localhost:8000/api/search?${params}`);
      const data: SearchResponse = await response.json();
      
      if (data.status === 'success') {
        setSearchResults(data.results);
        setOpensearchLogs(data.opensearch_logs);
      } else {
        setError('検索エラーが発生しました');
        setOpensearchLogs(data.opensearch_logs || null);
      }
    } catch (err) {
      setError('API接続エラーが発生しました');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const syncBlogs = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/sync-blogs');
      const data = await response.json();
      
      if (data.status === 'success') {
        alert('ブログデータをOpenSearchに同期しました');
      } else {
        alert('同期エラー: ' + data.message);
      }
    } catch (err) {
      alert('同期API呼び出しエラーが発生しました');
      console.error('Sync error:', err);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>ブログ検索システム</h1>
      
      <div style={{ marginBottom: '20px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2>検索フォーム</h2>
        
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="query" style={{ display: 'block', marginBottom: '5px' }}>
            検索クエリ:
          </label>
          <input
            id="query"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="検索したいキーワードを入力"
            style={{ 
              width: '100%', 
              padding: '8px', 
              border: '1px solid #ccc', 
              borderRadius: '4px',
              fontSize: '16px'
            }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="category" style={{ display: 'block', marginBottom: '5px' }}>
            カテゴリ:
          </label>
          <select
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            style={{ 
              padding: '8px', 
              border: '1px solid #ccc', 
              borderRadius: '4px',
              fontSize: '16px'
            }}
          >
            <option value="">すべて (news + poem)</option>
            <option value="news">News</option>
            <option value="poem">Poem</option>
          </select>
        </div>

        <div style={{ marginBottom: '15px' }}>
          <button
            onClick={handleSearch}
            disabled={loading}
            style={{
              padding: '10px 20px',
              backgroundColor: loading ? '#ccc' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontSize: '16px',
              marginRight: '10px'
            }}
          >
            {loading ? '検索中...' : '検索'}
          </button>

          <button
            onClick={syncBlogs}
            style={{
              padding: '10px 20px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px'
            }}
          >
            ブログデータ同期
          </button>
        </div>

        {error && (
          <div style={{ marginTop: '10px', color: 'red', fontWeight: 'bold' }}>
            {error}
          </div>
        )}
      </div>

      {searchResults.length > 0 && (
        <div style={{ marginBottom: '20px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h2>検索結果 ({searchResults.length}件)</h2>
          {searchResults.map((result) => (
            <div key={result.id} style={{ 
              marginBottom: '15px', 
              padding: '15px', 
              border: '1px solid #eee', 
              borderRadius: '4px',
              backgroundColor: '#f9f9f9'
            }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>{result.title}</h3>
              <p style={{ margin: '0 0 10px 0', color: '#666' }}>
                {result.content.substring(0, 200)}...
              </p>
              <div style={{ fontSize: '14px', color: '#888' }}>
                <span>カテゴリ: {result.category}</span> | 
                <span> スコア: {result.score?.toFixed(2)}</span> | 
                <span> 作成日: {new Date(result.created_at).toLocaleDateString('ja-JP')}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {opensearchLogs && (
        <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', backgroundColor: '#f5f5f5' }}>
          <h2>OpenSearch ログ</h2>
          <pre style={{ 
            backgroundColor: '#000', 
            color: '#00ff00', 
            padding: '15px', 
            borderRadius: '4px', 
            overflow: 'auto',
            fontSize: '12px',
            fontFamily: 'monospace'
          }}>
            {JSON.stringify(opensearchLogs, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
