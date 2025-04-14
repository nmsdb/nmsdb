from typing import Literal
from pydantic import BaseModel


class NavLink(BaseModel):
    type: Literal["htmx", "url_for", "href"] = "url_for"
    url: str


class NavigationGroup(BaseModel):
    nav_items: list["NavigationItem"] = []
    has_top_border: bool = False
    has_bottom_border: bool = False


class NavigationItemChild(BaseModel):
    title: str
    route: NavLink
    logo: str = None


class NavigationItem(BaseModel):
    title: str | None
    route: NavLink | None = None
    children: list[NavigationItemChild] = []
    logo: str | None = None
