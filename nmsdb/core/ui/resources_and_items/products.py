from typing import Annotated
from fastapi import APIRouter, Request, Depends

from nmsdb.main import templates
from nmsdb.core.navigation import NAV
from nmsdb.core.dependencies.database import DatabaseDep
from nmsdb.core.dependencies.redis import RedisServiceDep
from nmsdb.core.controllers.product import ProductControllerUI
from nmsdb.core.crud import nmsdb_product
from nmsdb.core.htmx import is_htmx
from nmsdb.core.models.product import ProductQueryParams as QueryParams


router = APIRouter()


@router.get("/")
async def ui_products_page(
    request: Request,
    db: DatabaseDep,
    redis: RedisServiceDep,
    skip: int = 0,
    limit: int = 100,
    q: Annotated[QueryParams, Depends()] = None,
):
    controller = ProductControllerUI(db=db, redis=redis, crud=nmsdb_product)

    if not is_htmx(request):
        return templates.TemplateResponse(
            request=request,
            name="pages/resources_and_items/products.html",
            context={
                "nav": NAV,
                "dropdown": await controller.build_type_dropdown(),
            },
        )

    products = await controller.get_multi(skip=skip, limit=limit, params=q)

    return templates.TemplateResponse(
        request=request,
        name="fragments/resources_and_items/products.html",
        context={
            "products": products,
        },
    )


@router.get("/{game_id}")
async def ui_product(
    request: Request, db: DatabaseDep, redis: RedisServiceDep, game_id: str
):
    controller = ProductControllerUI(db=db, redis=redis, crud=nmsdb_product)
    product = await controller.get(game_id=game_id)

    return templates.TemplateResponse(
        request=request,
        name="pages/resources_and_items/product.html",
        context={"nav": NAV, "product": product},
    )
