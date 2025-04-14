import re
from markupsafe import Markup, escape
from typing import Type

from sqlmodel import SQLModel, Field

from nmsdb.core.constants.nms import DESCRIPTION_TAG_STYLE_MAP
from nmsdb.core.models.params import QueryParams


class SubstanceBase(SQLModel):
    name: str
    name_lower: str
    game_id: str = Field(unique=True)
    symbol: str
    icon_file: str
    icon_path: str
    subtitle: str
    description: str
    base_value: int
    category: str
    rarity: str
    legality: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "UI_FUEL_1_NAME",
                "name_lower": "UI_FUEL_1_NAME_L",
                "game_id": "FUEL1",
                "symbol": "UI_FUEL1_SYM",
                "icon_file": "substance.fuel.1.png",
                "icon_path": "textures/ui/frontend/icons/u4substances",
                "subtitle": "UI_FUEL1_SUB",
                "description": "UI_FUEL_1_DESC",
                "base_value": 12,
                "category": "Fuel",
                "rarity": "Common",
                "legality": "Legal",
            }
        }

    def resolve_img_path(self):
        return f"img/{self.icon_path}/{self.icon_file}"

    @property
    def ui_description(self) -> Markup:
        desc = escape(self.description)

        for tag, css_class in DESCRIPTION_TAG_STYLE_MAP.items():
            pattern = rf"&lt;{tag}&gt;(.*?)&lt;&gt;"
            replacement = rf'<a class="{css_class}" href="#">{r"\1"}</a>'
            desc = re.sub(pattern, replacement, desc)

        desc = desc.replace("\n", "<br>")
        return Markup(desc)


class SubstanceCreate(SubstanceBase):
    pass


class SubstanceRead(SubstanceBase):
    pass


class SubstanceUpdate(SubstanceBase):
    pass


class Substance(SubstanceBase, table=True):
    id: int = Field(primary_key=True)


class SubstanceQueryParams(QueryParams):
    name: str | None = None
    game_id: str | None = None
    name_lower: str | None = None
    category: str | None = None
    type: str | None = None
    rarity: str | None = None
    legality: str | None = None
