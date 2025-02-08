from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from app.presentation.routers import item_router
from dotenv import load_dotenv
from app.infrastructure.db.session import engine
from app.presentation.admin.model_views import ItemModelView
load_dotenv()

app = FastAPI(title="Sample API", description="This is a sample API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Add Admin
admin = Admin(app, engine=engine)
admin.add_model_view(ItemModelView)

app.include_router(item_router.router)
@app.get("/health")
def health():
    return {"status": "ok"}