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

@web_router.get("/web/error")
def error_page():
    return FileResponse("static/error.html")


@web_router.get("/web/{path:path}")
def serve(path: str | None = None):
    file_path = "static/index.html" if not path else f"static/{path}"
    if not os.path.exists(file_path):
        return RedirectResponse(url="/web/error")
    return FileResponse(file_path)
