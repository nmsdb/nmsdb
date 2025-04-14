from typing import Annotated

from fastapi import APIRouter, Depends

from nmsdb.core.models.substance import SubstanceRead
from nmsdb.core.models.substance import SubstanceQueryParams as QueryParams
from nmsdb.core.dependencies.database import DatabaseDep
from nmsdb.core.dependencies.redis import RedisServiceDep
from nmsdb.core.controllers.substance import SubstanceControllerAPI
from nmsdb.core.crud import nmsdb_substance

router = APIRouter()


@router.get("/", response_model=list[SubstanceRead])
async def get_substances(
    db: DatabaseDep,
    redis: RedisServiceDep,
    skip: int = 0,
    limit: int = 100,
    params: Annotated[QueryParams, Depends()] = None,
):
    controller = SubstanceControllerAPI(db=db, redis=redis, crud=nmsdb_substance)
    return await controller.get_multi(skip=skip, limit=limit, params=params)


@router.get("/{game_id}", response_model=SubstanceRead)
async def get_substance(db: DatabaseDep, redis: RedisServiceDep, game_id: str):
    controller = SubstanceControllerAPI(db=db, redis=redis, crud=nmsdb_substance)
    return await controller.get(game_id=game_id)
