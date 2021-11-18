from fastapi import APIRouter

from controllers import products_controller

router = APIRouter()

router.include_router(products_controller.router)