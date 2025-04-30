from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from .api import router as api_router

base_router = APIRouter()

routers = [base_router, api_router]
