from pydantic import BaseModel

from nmsdb.core.models.htmx import HTMXSwapAction, HTMXTrigger


class HTMXDropdownItem(BaseModel):
    label: str
    value: str


class HTMXDropdown(BaseModel):
    name: str
    url: str
    items: list[HTMXDropdownItem]
    action: HTMXSwapAction = HTMXSwapAction.INNER_HTML
    trigger: HTMXTrigger = HTMXTrigger.CHANGE
    target: str
