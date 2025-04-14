from fastapi import APIRouter

CoreUIController = APIRouter(include_in_schema=False)

from nmsdb.core.ui.resources_and_items import (
    products,
    substances,
)

CoreUIController.include_router(products.router, prefix="/products", tags=["Products"])
CoreUIController.include_router(
    substances.router, prefix="/substances", tags=["Substances"]
)
