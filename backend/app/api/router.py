from fastapi import APIRouter

from app.api import auth, bom, breviar, calcule, catalog, circuite, proiecte, receptori, schema, tablouri

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(proiecte.router)
api_router.include_router(tablouri.router)
api_router.include_router(circuite.router)
api_router.include_router(receptori.router)
api_router.include_router(calcule.router)
api_router.include_router(catalog.router)
api_router.include_router(schema.router)
api_router.include_router(bom.router)
api_router.include_router(breviar.router)
