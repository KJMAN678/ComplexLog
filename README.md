### Devin

- [Devin's Machine](https://app.devin.ai/workspace) でリポジトリ追加

#### 1.Git Pull
- そのまま

#### 2.Configure Secrets
```sh
# 環境変数用のファイル作成
$ touch .envrc

# .envrc に下記を入力. xxx は適宜更新

export DJANGO_SUPERUSER_USERNAME=xxx
export DJANGO_SUPERUSER_EMAIL=xxx@xxx.com
export DJANGO_SUPERUSER_PASSWORD=xxx
export OPENSEARCH_INITIAL_ADMIN_PASSWORD=xxx
export BACKEND_URL=http://localhost:8000

# 環境変数を読み込む
$ direnv allow
```

- ローカル用
```sh
$ brew install direnv
```
#### 4.Maintain Dependencies
```sh
# ローカルM1Mac用
$ docker compose -f docker-compose.mac.yaml up -d
# Devin用
$ docker compose -f docker-compose.ubuntu.yaml up -d


# コンテナ作り直し
$ ./remake-container.sh mac
$ ./remake-container.sh ubuntu
```

#### 5.SetUp Lint
```sh
# ローカルM1Mac用
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run ruff check .
$ docker compose -f docker-compose.mac.yaml run --rm frontend npx next lint

# Devin用
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run ruff check .
$ docker compose -f docker-compose.ubuntu.yaml run --rm frontend npx next lint
```

#### 6.SetUp Tests
- no tests ran in 0.00s だと Devin の Verify が通らないっぽい
```sh
# ローカルM1Mac用
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run pytest
$ docker compose -f docker-compose.mac.yaml run --rm frontend npm run test

# Devin用
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run pytest
$ docker compose -f docker-compose.ubuntu.yaml run --rm frontend npm run test

# ローカルM1Mac用
# 一度実行 ブラウザのインストール
$ docker compose -f docker-compose.mac.yaml run --rm frontend npx playwright install firefox
# Playwright
$ docker compose -f docker-compose.mac.yaml run --rm frontend npx playwright test --project firefox

# Devin用
# 一度実行 ブラウザのインストール
$ docker compose -f docker-compose.ubuntu.yaml run --rm frontend npx playwright install firefox
# Playwright
$ docker compose -f docker-compose.ubuntu.yaml run --rm frontend npx playwright test --project firefox
```

### 7.Setup Local App

```sh
$ http://localhost:3000/ がフロントエンドのURL
$ http://localhost:8000/ がバックエンドのURL
$ http://localhost:5601/ が OpenSearch-Dashboards のURL
```

#### 8.Additional Notes
- 必ず日本語で回答してください
を入力

### OPENAI-API で PR-Review
- [Qodo Merge](https://qodo-merge-docs.qodo.ai/installation/github/)
  - GPT-4.1利用
  - 日本語の回答をするようプロンプト設定
- GitHub の Repository >> Settings >> Secretes and variables >> Actions の Repository secrets の New repository secret を登録
  - OPENAI_KEY という名称で OPENAI API keys の SECRET KEY を登録
    - [OPENAI API keys](https://platform.openai.com/settings/organization/api-keys) 
```sh
--- .github/
           |- workflows/
                        |-- pr_agent.yml
```
### Django
- app 追加
```sh
# ローカルM1Mac用
$ mkdir -p backend/app/api
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run django-admin startapp api app/api
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run python app/manage.py makemigrations
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run python app/manage.py migrate

# Devin用
$ mkdir -p backend/app/api
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run django-admin startapp api app/api
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run python app/manage.py makemigrations
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run python app/manage.py migrate
```

- データ作成
```sh
# ローカルM1Mac用
$ docker compose -f docker-compose.mac.yaml run --rm backend uv run python app/manage.py create_blog_data 100

# Devin用
$ docker compose -f docker-compose.ubuntu.yaml run --rm backend uv run python app/manage.py create_blog_data 100
```

### OpenSearch サンプルログ

<details><summary>OpenSearch サンプルログ</summary>
```sh
{
  "query": {
    "query": {
      "bool": {
        "must": [
          {
            "multi_match": {
              "query": "ストレージ",
              "fields": [
                "title^2",
                "content"
              ],
              "type": "best_fields"
            }
          },
          {
            "term": {
              "category": "poem"
            }
          }
        ]
      }
    },
    "size": 20,
    "sort": [
      {
        "created_at": {
          "order": "desc"
        }
      }
    ]
  },
  "response_time": 4,
  "total_hits": 4,
  "max_score": null,
  "raw_response": {
    "took": 4,
    "timed_out": false,
    "_shards": {
      "total": 1,
      "successful": 1,
      "skipped": 0,
      "failed": 0
    },
    "hits": {
      "total": {
        "value": 4,
        "relation": "eq"
      },
      "max_score": null,
      "hits": [
        {
          "_index": "blogs",
          "_id": "87",
          "_score": null,
          "_source": {
            "title": "軸仕上げ探査電池運。",
            "content": "建築ダニヒール人形証言する式持ってる革新参加する彼。\n日曜日ハンマー評議会見落とす大統領状況日曜日転倒。\n彼通行料金デッドコピージャーナル参加する大統領〜。\n尿陶器ブラケット暖かいストレージ指名試してみる犯罪者。",
            "category": "poem",
            "created_at": "2025-07-12T23:49:15.148848+00:00"
          },
          "sort": [
            1752364155148
          ]
        },
        {
          "_index": "blogs",
          "_id": "85",
          "_score": null,
          "_source": {
            "title": "偏差助けて省略指名。",
            "content": "高いオークション野球怒り今オークション。\n主婦敵対的なストレージパイオニアソース。\n持ってるストレージ犯罪者タワーブランチ追放する本質的な脊椎。\nジャーナル主人インチバケツマリン。",
            "category": "poem",
            "created_at": "2025-07-12T23:49:15.148318+00:00"
          },
          "sort": [
            1752364155148
          ]
        },
        {
          "_index": "blogs",
          "_id": "77",
          "_score": null,
          "_source": {
            "title": "近代化するベルベット見落とすストレージチーズ。",
            "content": "トーンコピー脊椎雪君は大統領ない創傷中世スマッシュ。\nコピー協力自体目的ストレージ。\n偏差彼花嫁持っていました指名符号電話状況。\nあなた自身動物動物叔父画面革新。",
            "category": "poem",
            "created_at": "2025-07-12T23:49:15.145792+00:00"
          },
          "sort": [
            1752364155145
          ]
        },
        {
          "_index": "blogs",
          "_id": "70",
          "_score": null,
          "_source": {
            "title": "柔らかいそれ。",
            "content": "叔父偏差敵創傷部隊供給索引リフト数字擁する。\n中世は脊椎憲法持ってるそれ編組デッドキャビネット。\nヘア屋根裏ストレージ犯罪者極端な。\n電池運埋め込む本質的な彼女教会。",
            "category": "poem",
            "created_at": "2025-07-12T23:49:15.142386+00:00"
          },
          "sort": [
            1752364155142
          ]
        }
      ]
    }
  }
}
```
</details>

### 参考文献

#### Docker Compose
- [Compose Build Specification](https://docs.docker.com/compose/compose-file/build)
- [Compose で起動とシャットダウンの順序を制御する](https://docs.docker.com/compose/startup-order/)
  - Health Check
    - [docker-compose-healthcheck](https://github.com/peter-evans/docker-compose-healthcheck/blob/master/README.md)
    - [OpenSearch Cluster health](http://docs.opensearch.org/docs/latest/api-reference/cluster-api/cluster-health/)
    - [PostgreSQL pg_isready](https://www.postgresql.org/docs/9.4/app-pg-isready.html)
- Network
  - [Compose networks](https://docs.docker.com/compose/networks/)
  - [Compose volumes](https://docs.docker.com/compose/volumes/)
