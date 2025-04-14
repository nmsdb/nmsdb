import re
from markupsafe import Markup, escape
from typing import Optional, Type

from sqlmodel import SQLModel, Field

from nmsdb.core.constants.nms import DESCRIPTION_TAG_STYLE_MAP
from nmsdb.core.models.params import QueryParams


class ProductBase(SQLModel):
    name: str
    name_lower: str
    game_id: str = Field(unique=True)
    icon_file: str
    icon_path: str
    subtitle: str
    description: str
    base_value: int
    category: str = Field(description="Category of the product")
    type: str
    rarity: str
    legality: str
    craftable: bool

    class Config:
        json_schema_extra = {"example": {}}

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


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase, table=True):
    id: int = Field(primary_key=True)


class ProductQueryParams(QueryParams):
    name: Optional[str] = None
    game_id: Optional[str] = None
    name_lower: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None
    rarity: Optional[str] = None
    legality: Optional[str] = None
