from typing import Annotated
from fastapi import APIRouter, Request, Depends

from nmsdb.core.dependencies.database import DatabaseDep
from nmsdb.core.dependencies.redis import RedisServiceDep
from nmsdb.core.controllers.product import ProductControllerUI
from nmsdb.core.crud import nmsdb_product
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
    return await controller.get_objects(request, skip, limit, q)


@router.get("/{game_id}")
async def ui_product(
    request: Request, db: DatabaseDep, redis: RedisServiceDep, game_id: str
):
    controller = ProductControllerUI(db=db, redis=redis, crud=nmsdb_product)
    return await controller.get_object(request, game_id)
