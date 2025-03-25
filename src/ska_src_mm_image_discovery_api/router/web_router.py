import os

from fastapi import APIRouter
from starlette.responses import FileResponse, RedirectResponse

web_router = APIRouter(
    tags=["web"]
)


# redirection rule
@web_router.get("/")
def home():
    return RedirectResponse(url="/web/")

@web_router.get("/assets/{path:path}")
def home(path: str):
    return RedirectResponse(f"/web/assets/{path}")


@web_router.get("/web/error")
def error_page():
    return RedirectResponse('/')


@web_router.get("/web/{path:path}")
def serve(path: str | None = None):
    file_path = "ui/dist/index.html" if not path else f"ui/dist/{path}"
    if not os.path.exists(file_path):
        return RedirectResponse(url="/web/error")
    return FileResponse(file_path)
