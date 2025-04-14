from fastapi import APIRouter

APIController = APIRouter()


from nmsdb.core.api.resources_and_items import products, substances

APIController.include_router(
    products.router, prefix="/products", tags=["Resources and Items"]
)
APIController.include_router(
    substances.router, prefix="/substances", tags=["Resources and Items"]
)
