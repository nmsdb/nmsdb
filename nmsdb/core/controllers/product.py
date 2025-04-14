from fastapi import HTTPException, status, Request

from nmsdb.main import app, templates
from nmsdb.core.navigation import NAV
from nmsdb.core.controllers.base import (
    BaseController,
    BaseUIController,
    BaseAPIController,
)
from nmsdb.core.models.product import Product, ProductQueryParams
from nmsdb.core.crud.product import CRUDProduct
from nmsdb.core.constants.redis import REDIS_KEY_SUBSTANCE, REDIS_KEY_LANGUAGE_ENGLISH
from nmsdb.core.models.ui.dropdown import HTMXDropdown, HTMXDropdownItem
from nmsdb.core.dependencies.redis import get_redis_service
from nmsdb.core.constants.redis import REDIS_KEY_PRODUCT_TYPES
from nmsdb.core.htmx import is_htmx


class ProductControllerBase(BaseController):
    CRUDController = CRUDProduct

    async def _get(self, game_id: str) -> Product:
        """
        Get a product by game_id, with caching.

        Args:
            game_id: The game ID of the product
            cache_timeout: Cache expiration time in seconds (default: 1 hour)

        Returns:
            Product object
        """
        cache_key = REDIS_KEY_SUBSTANCE.format(game_id=game_id)

        product = await self.cache_get(
            cache_key=cache_key,
            fetch_data_func=self.crud.get_by_game_id,
            db=self.db,
            game_id=game_id,
        )

        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found.")

        keys = await self.redis.get_multi(
            [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.name),
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.name_lower),
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.subtitle),
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.description),
            ]
        )

        name_value = keys.get(REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.name))
        if name_value is not None:
            product.name = name_value

        name_lower_value = keys.get(
            REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.name_lower)
        )
        if name_lower_value is not None:
            product.name_lower = name_lower_value

        subtitle_value = keys.get(
            REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.subtitle)
        )
        if subtitle_value is not None:
            product.subtitle = subtitle_value

        description_value = keys.get(
            REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.description)
        )
        if description_value is not None:
            product.description = description_value

        return product

    async def _get_multi(
        self, skip: int = 0, limit: int = 100, params: ProductQueryParams | None = None
    ) -> list[Product]:
        products = await self.crud.get_multi(
            self.db, skip=skip, limit=limit, params=params
        )

        keys = await self.redis.get_multi(
            [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.name)
                for product in products
            ]
            + [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.name_lower)
                for product in products
            ]
            + [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.subtitle)
                for product in products
            ]
            + [
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.description)
                for product in products
            ]
        )

        for product in products:
            name_value = keys.get(
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.name)
            )
            if name_value is not None:
                product.name = name_value

            name_lower_value = keys.get(
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.name_lower)
            )
            if name_lower_value is not None:
                product.name_lower = name_lower_value

            subtitle_value = keys.get(
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.subtitle)
            )
            if subtitle_value is not None:
                product.subtitle = subtitle_value

            description_value = keys.get(
                REDIS_KEY_LANGUAGE_ENGLISH.format(word_id=product.description)
            )
            if description_value is not None:
                product.description = description_value

        return products


class ProductControllerAPI(BaseAPIController, ProductControllerBase):
    async def get_object(self, game_id: str) -> Product:
        return await super()._get(game_id=game_id)

    async def get_objects(
        self, skip: int = 0, limit: int = 100, params: ProductQueryParams | None = None
    ) -> list[Product]:
        return await super()._get_multi(skip=skip, limit=limit, params=params)


class ProductControllerUI(BaseUIController, ProductControllerBase):
    async def get_object(self, request: Request, game_id: str) -> Product:
        product = await super()._get(game_id=game_id)
        return templates.TemplateResponse(
            request=request,
            name="pages/resources_and_items/product.html",
            context={"nav": NAV, "product": product},
        )

    async def get_objects(
        self,
        request: Request,
        skip: int = 0,
        limit: int = 100,
        params: ProductQueryParams | None = None,
    ) -> list[Product]:
        if not is_htmx(request):
            return templates.TemplateResponse(
                request=request,
                name="pages/resources_and_items/products.html",
                context={
                    "nav": NAV,
                    "dropdown": await self.build_type_dropdown(),
                },
            )

        products = await super()._get_multi(skip=skip, limit=limit, params=params)
        return templates.TemplateResponse(
            request=request,
            name="fragments/resources_and_items/products.html",
            context={
                "products": products,
            },
        )

    async def build_type_dropdown(self) -> HTMXDropdown:
        """
        Build the dropdown for the products page to filter by Category.
        """
        redis = get_redis_service()
        product_types = await redis.get_list(REDIS_KEY_PRODUCT_TYPES)

        return HTMXDropdown(
            name="type",
            target="#products-container",
            url=app.url_path_for("ui_products_page"),
            items=[
                HTMXDropdownItem(label="All", value=""),
                *[
                    HTMXDropdownItem(label=product_type, value=product_type)
                    for product_type in product_types
                ],
            ],
        )
