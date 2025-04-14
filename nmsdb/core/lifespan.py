from contextlib import asynccontextmanager
from typing import Set

from fastapi import FastAPI

from nmsdb.core.dependencies.database import SessionLocal
from nmsdb.core.dependencies.redis import get_redis_service
from nmsdb.core.crud import nmsdb_product, nmsdb_substance
from nmsdb.core.constants.redis import (
    REDIS_KEY_PRODUCT_TYPES,
    REDIS_KEY_SUBSTANCE_CATEGORIES,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = get_redis_service()

    async with SessionLocal() as session:
        substances = await nmsdb_substance.get_multi(db=session, limit=0)
        products = await nmsdb_product.get_multi(db=session, limit=0)

    substance_categories: Set[str] = {substance.category for substance in substances}
    product_types: Set[str] = {product.type for product in products}

    # Also create summary sets
    await redis.delete(REDIS_KEY_SUBSTANCE_CATEGORIES, REDIS_KEY_PRODUCT_TYPES)

    if substance_categories:
        await redis.push_list(
            REDIS_KEY_SUBSTANCE_CATEGORIES, *list(substance_categories)
        )

    if product_types:
        await redis.push_list(REDIS_KEY_PRODUCT_TYPES, *list(product_types))

    print(
        f"Pre-seeded Redis with {len(substance_categories)} substance categories and {len(product_types)} product types"
    )

    yield
