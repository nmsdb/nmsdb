from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from nmsdb.config import settings
from nmsdb.core.navigation import NAV
from nmsdb.core.lifespan import lifespan


templates = Jinja2Templates(
    directory=(
        "nmsdb/core/templates",
        "nmsdb/modules/substances",
    )
)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="nmsdb/core/static"), name="static")


@app.middleware("http")
async def maintenance_mode(request: Request, call_next):
    response = await call_next(request)
    if settings.MAINTENANCE_MODE and not request.url.path.startswith("/static/"):
        return templates.TemplateResponse(
            request=request, name="pages/maintenance.html", context={"nav": NAV}
        )

    return response


@app.get("/", include_in_schema=False)
async def landing_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="pages/landing_page.html", context={"nav": NAV}
    )


from nmsdb.core.ui import CoreUIController
from nmsdb.core.api import APIController

app.include_router(APIController, prefix="/api/v1")
app.include_router(CoreUIController)
