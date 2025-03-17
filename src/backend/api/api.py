from fastapi import APIRouter
from api.endpoints import auth, columns, listvalues, items

router = APIRouter()

router.include_router(columns.router, prefix='/columns')
router.include_router(listvalues.router, prefix='/listvalues')
router.include_router(items.router, prefix='/items')
router.include_router(auth.router, prefix='/auth')