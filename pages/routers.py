from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["pages"],
    prefix="/page",
)
templates = Jinja2Templates(directory="static")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})
