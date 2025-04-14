from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from nmsdb.core.crud.base import CRUDBase
from nmsdb.core.models.product import Product, ProductUpdate, ProductCreate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    async def get_by_name(self, db: AsyncSession, name: str) -> list[Product] | None:
        """Get product by name.

        Args:
            db:             SQLModel Session.
            name:           Product name.
        """
        product = await db.exec(select(Product).where(Product.name == name))
        return product.all()

    async def get_by_game_id(self, db: AsyncSession, game_id: str) -> Product | None:
        """Get product by game_id.

        Args:
            db:             SQLModel Session.
            game_id:        Product game_id.
        """
        product = await db.exec(select(Product).where(Product.game_id == game_id))
        return product.first()


nmsdb_product = CRUDProduct(Product)
