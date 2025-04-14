from typing import Annotated
from fastapi import APIRouter, Request, Depends

from nmsdb.main import templates
from nmsdb.core.navigation import NAV
from nmsdb.core.dependencies.database import DatabaseDep
from nmsdb.core.dependencies.redis import RedisServiceDep
from nmsdb.core.controllers.substance import SubstanceControllerUI
from nmsdb.core.crud import nmsdb_substance
from nmsdb.core.htmx import is_htmx
from nmsdb.core.models.substance import SubstanceQueryParams as QueryParams

router = APIRouter()


@router.get("/")
async def ui_substances_page(
    request: Request,
    db: DatabaseDep,
    redis: RedisServiceDep,
    skip: int = 0,
    limit: int = 100,
    params: Annotated[QueryParams, Depends()] = None,
):
    controller = SubstanceControllerUI(db=db, redis=redis, crud=nmsdb_substance)
    if not is_htmx(request):
        return templates.TemplateResponse(
            request=request,
            name="pages/resources_and_items/substances.html",
            context={
                "nav": NAV,
                "dropdown": await controller.build_category_dropdown(),
            },
        )

    substances = await controller.get_multi(skip=skip, limit=limit, params=params)

    return templates.TemplateResponse(
        request=request,
        name="fragments/resources_and_items/substances.html",
        context={"substances": substances},
    )


@router.get("/{game_id}")
async def ui_substance(
    request: Request, db: DatabaseDep, redis: RedisServiceDep, game_id: str
):
    controller = SubstanceControllerUI(db=db, redis=redis, crud=nmsdb_substance)
    substance = await controller.get(game_id=game_id)

    return templates.TemplateResponse(
        request=request,
        name="pages/resources_and_items/substance.html",
        context={"nav": NAV, "substance": substance},
    )
