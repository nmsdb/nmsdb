from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from nmsdb.core.crud.base import CRUDBase
from nmsdb.core.models.substance import Substance, SubstanceUpdate, SubstanceCreate


class CRUDSubstance(CRUDBase[Substance, SubstanceCreate, SubstanceUpdate]):
    async def get_by_name(self, db: AsyncSession, name: str) -> list[Substance] | None:
        """Get substance by name.

        Args:
            db:             SQLModel Session.
            name:           Substance name.
        """
        substance = await db.exec(select(Substance).where(Substance.name == name))
        return substance.all()

    async def get_by_game_id(self, db: AsyncSession, game_id: str) -> Substance | None:
        """Get substance by game_id.

        Args:
            db:             SQLModel Session.
            game_id:        Substance game_id.
        """
        substance = await db.exec(select(Substance).where(Substance.game_id == game_id))
        return substance.first()


nmsdb_substance = CRUDSubstance(Substance)
