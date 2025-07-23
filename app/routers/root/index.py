from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse

from app.core.templates import templates

router = APIRouter(prefix="", tags=["Root"])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "root/index.html",
        {"request": request, "title": "RFID MIDDLEWARE"},
    )
