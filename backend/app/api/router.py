from fastapi import APIRouter

from app.api import auth, calcule, circuite, proiecte, receptori, tablouri

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(proiecte.router)
api_router.include_router(tablouri.router)
api_router.include_router(circuite.router)
api_router.include_router(receptori.router)
api_router.include_router(calcule.router)
