from enum import Enum


class HTMXSwapAction(str, Enum):
    INNER_HTML = "innerHTML"
    OUTER_HTML = "outerHTML"
    BEFORE_BEGIN = "beforebegin"
    AFTER_BEGIN = "afterbegin"
    BEFORE_END = "beforeend"
    AFTER_END = "afterend"
    DELETE = "delete"
    NONE = "none"


class HTMXTrigger(str, Enum):
    CLICK = "click"
    CHANGE = "change"
    SUBMIT = "submit"
    LOAD = "load"
    EVERY = "every"
    NONE = "none"
