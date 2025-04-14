from fastapi import HTTPException, status, Request

from nmsdb.main import app, templates
from nmsdb.core.navigation import NAV
from nmsdb.core.controllers.base import (
    BaseController,
    BaseUIController,
    BaseAPIController,
)
from nmsdb.core.models.substance import Substance, SubstanceQueryParams
from nmsdb.core.crud.substance import CRUDSubstance
from nmsdb.core.constants.redis import REDIS_KEY_SUBSTANCE, REDIS_KEY_LANGUAGE_ENGLISH
from nmsdb.core.models.ui.dropdown import HTMXDropdown, HTMXDropdownItem
from nmsdb.core.dependencies.redis import get_redis_service
from nmsdb.core.constants.redis import REDIS_KEY_SUBSTANCE_CATEGORIES
from nmsdb.core.htmx import is_htmx


class SubstanceControllerBase(BaseController):
    async def _get(self, game_id: str) -> Substance:
        """
        Get a substance by game_id, with caching.

        Args:
            game_id: The game ID of the substance
            cache_timeout: Cache expiration time in seconds (default: 1 hour)

        Returns:
            Substance object
        """
        cache_key = REDIS_KEY_SUBSTANCE.format(game_id=game_id)

        substance = await self.cache_get(
            cache_key=cache_key,
            fetch_data_func=self.crud.get_by_game_id,
            db=self.db,
            game_id=game_id,
        )

        if not substance:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="Substance not found."
            )

        keys = await self.redis.get_multi(
            [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.name),
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.name_lower),
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.symbol),
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.subtitle),
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.description),
            ]
        )

        name_value = keys.get(REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.name))
        if name_value is not None:
            substance.name = name_value

        name_lower_value = keys.get(
            REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.name_lower)
        )
        if name_lower_value is not None:
            substance.name_lower = name_lower_value

        symbol_value = keys.get(
            REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.symbol)
        )
        if symbol_value is not None:
            substance.symbol = symbol_value

        subtitle_value = keys.get(
            REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.subtitle)
        )
        if subtitle_value is not None:
            substance.subtitle = subtitle_value

        description_value = keys.get(
            REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.description)
        )
        if description_value is not None:
            substance.description = description_value

        return substance

    async def _get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        params: SubstanceQueryParams | None = None,
    ) -> list[Substance]:
        substances = await self.crud.get_multi(
            self.db, skip=skip, limit=limit, params=params
        )

        keys = await self.redis.get_multi(
            [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.name)
                for substance in substances
            ]
            + [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.name_lower)
                for substance in substances
            ]
            + [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.symbol)
                for substance in substances
            ]
            + [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.subtitle)
                for substance in substances
            ]
            + [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.description)
                for substance in substances
            ]
        )

        for substance in substances:
            name_value = keys.get(
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.name)
            )
            if name_value is not None:
                substance.name = name_value

            name_lower_value = keys.get(
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.name_lower)
            )
            if name_lower_value is not None:
                substance.name_lower = name_lower_value

            symbol_value = keys.get(
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.symbol)
            )
            if symbol_value is not None:
                substance.symbol = symbol_value

            subtitle_value = keys.get(
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.subtitle)
            )
            if subtitle_value is not None:
                substance.subtitle = subtitle_value

            description_value = keys.get(
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=substance.description)
            )
            if description_value is not None:
                substance.description = description_value

        return substances


class SubstanceControllerAPI(BaseAPIController, SubstanceControllerBase):
    CRUDController = CRUDSubstance

    async def get_object(self, game_id: str) -> Substance:
        return await super()._get(game_id=game_id)

    async def get_objects(
        self,
        skip: int = 0,
        limit: int = 100,
        params: SubstanceQueryParams | None = None,
    ) -> list[Substance]:
        return await super()._get_multi(skip=skip, limit=limit, params=params)


class SubstanceControllerUI(BaseUIController, SubstanceControllerBase):
    async def get_object(self, request: Request, game_id: str) -> Substance:
        substance = await self._get(game_id=game_id)
        return templates.TemplateResponse(
            request=request,
            name="pages/resources_and_items/substance.html",
            context={"nav": NAV, "substance": substance},
        )

    async def get_objects(
        self,
        request: Request,
        skip: int = 0,
        limit: int = 100,
        params: SubstanceQueryParams | None = None,
    ) -> list[Substance]:
        if not is_htmx(request):
            return templates.TemplateResponse(
                request=request,
                name="pages/resources_and_items/substances.html",
                context={
                    "nav": NAV,
                    "dropdown": await self.build_category_dropdown(),
                },
            )

        substances = await self._get_multi(skip=skip, limit=limit, params=params)

        return templates.TemplateResponse(
            request=request,
            name="fragments/resources_and_items/substances.html",
            context={"substances": substances},
        )

    async def build_category_dropdown(self) -> HTMXDropdown:
        """
        Build the dropdown for the substances page to filter by Category.
        """
        redis = get_redis_service()
        categories = await redis.get_list(REDIS_KEY_SUBSTANCE_CATEGORIES)

        return HTMXDropdown(
            name="category",
            target="#substances-container",
            url=app.url_path_for("ui_substances_page"),
            items=[
                HTMXDropdownItem(label="All", value=""),
                *[
                    HTMXDropdownItem(label=category, value=category)
                    for category in categories
                ],
            ],
        )
