from typing import Annotated

from fastapi import APIRouter, Depends

from nmsdb.core.models.product import ProductRead
from nmsdb.core.models.product import ProductQueryParams as QueryParams
from nmsdb.core.dependencies.database import DatabaseDep
from nmsdb.core.dependencies.redis import RedisServiceDep
from nmsdb.core.controllers.product import ProductControllerAPI
from nmsdb.core.crud import nmsdb_product

router = APIRouter()


@router.get("/", response_model=list[ProductRead])
async def get_products(
    db: DatabaseDep,
    redis: RedisServiceDep,
    skip: int = 0,
    limit: int = 100,
    q: Annotated[QueryParams, Depends()] = None,
):
    controller = ProductControllerAPI(db=db, redis=redis, crud=nmsdb_product)
    return await controller.get_objects(skip=skip, limit=limit, params=q)


@router.get("/{game_id}", response_model=ProductRead)
async def get_product(db: DatabaseDep, redis: RedisServiceDep, game_id: str):
    controller = ProductControllerAPI(db=db, redis=redis, crud=nmsdb_product)
    return await controller.get_object(game_id=game_id)
