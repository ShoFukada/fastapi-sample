# fastAPIオニオンアーキテクチャサンプル
## オニオンアーキテクチャについて
### 主な層
- Presentation
    - api endpoint (router controller)
    - req,res schema
- Application Services
    - =usecase
- Domain
    - Domain Service
        - ビジネスロジック
        - Infra層のinterface実装
    - Domain Model
        - Entity
        - Value Object
-  Infrastructure
    - 外部API
    - DB
        - Repository(domain層のImpl)
        - db_model
### 依存関係
```
[Presentation Layer]  
       ↓ (UseCaseを呼び出す)
[Application Layer (UseCase)]  
       ↓ (Domainのビジネスロジックを利用)
[Domain Layer]  
       ↓ (Interfaceを通じて利用)
[Infrastructure Layer]  
```
## 立ち上げ
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic init alembic
uvicorn app.main:app --reload
```

### sql関連
- sqlArchemyの設定
    - db/session.pyにて初期化コード
- alembic
    - https://zenn.dev/shimakaze_soft/articles/4c0784d9a87751
alembic初期化
```
alembic init alembic
```
- dbとの紐付け→env.pyに記述
- metadataの紐付け→env.pyに記載
- マイグレーションファイルの作成(gitのcommit的な、versions配下にたまる)
```
alembic revision --autogenerate -m "create items table"
```
- マイグレーションファイルの反映
```
alembic upgrade head
```

## ディレクトリ構造

## その他Tips
- SQLAlchemy→ORM
    - import Columnとか
- Alembic→マイグレーション管理(スキーマの変更履歴の管理)

## TODO
- tests
- DI
- chatbotなど外部ロジック含めて見る