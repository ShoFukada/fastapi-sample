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

## DIについて
https://zenn.dev/ktnyt/articles/cc5056ce81e9d3
- Injector
    - 型をキーとして値を提供するdictのようなもの
- Binder
    - どの抽象をどの実装にバインドするか
- Module
    - diの紐付けを記述するクラス？

- 元々→router部分で、repositoryのインスタンス化→repositoryをusecaseに入れてusecaseをインスタンス化してる。
- これをinjector.getに変更する

### @injectについて
- @injectをつけると、injectorは型ヒントから自動でbindを確認してインスタンスを自動で渡すようになる
```python
class ItemUseCase:
    @inject
    def __init__(self, item_repository: ItemRepositoryInterface):
        self.item_repository = item_repository

class AppModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(ItemRepositoryInterface, to=ItemRepository, scope=singleton)
        binder.bind(ItemUseCase, scope=singleton)

injector = Injector([AppModule()])
```
ItemUseCaseの生成→@injectがあるためitemrepositoryinterfaceのbind先を探す→itemrepositoryにbindされているためそれから作成する

### @providerについて
- 手動でinterfaceとの紐付けを書く
```python
class AppModule(Module):
    @provider
    def provide_item_repository(self) -> ItemRepositoryInterface:
        return ItemRepository()

    @provider
    def provide_item_usecase(self, repo: ItemRepositoryInterface) -> ItemUseCase:
        """UseCaseの生成ロジック。ここで何を引数にとるかが依存関係になる"""
        return ItemUseCase(repo)
```

## ディレクトリ構造

## その他Tips
- SQLAlchemy→ORM
    - import Columnとか
- Alembic→マイグレーション管理(スキーマの変更履歴の管理)

## TODO
- chatmessages endpoint
- user auth