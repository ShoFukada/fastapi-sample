import logging
import sys
from logging.config import dictConfig

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

# ルーターやAdminビューをインポート
from app.presentation.routers import item_router, chat_router, user_router
from app.infrastructure.db.session import engine
from app.presentation.admin.model_views import (
    ItemModelView,
    UserModelView,
    ChatSessionModelView,
    ChatMessageModelView,
    RetrievedDocModelView
)

# ログ設定ファイルをインポート
from app.core.logging import setup_logging

# 1) ログ設定を先に適用
setup_logging()

# 2) FastAPIアプリ作成
app = FastAPI(
    title="Sample API",
    description="This is a sample API",
    version="0.1.0"
)

# 3) 例外をキャッチしてログを出すミドルウェア
@app.middleware("http")
async def log_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        logging.exception("Unhandled exception occurred in request.")
        # ここで再raiseしないとFastAPIが普通にエラーを返さないため再度raise
        raise

# 4) CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5) sqladmin の登録
admin = Admin(app, engine=engine)
admin.add_model_view(ItemModelView)
admin.add_model_view(UserModelView)
admin.add_model_view(ChatSessionModelView)
admin.add_model_view(ChatMessageModelView)
admin.add_model_view(RetrievedDocModelView)

# 6) ルーターの登録
app.include_router(item_router.router)
app.include_router(chat_router.router)
app.include_router(user_router.router)

@app.get("/health")
def health():
    return {"status": "ok"}