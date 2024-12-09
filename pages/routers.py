from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["pages"],
    prefix="/page",
)
templates = Jinja2Templates(directory="static")


@router.get("/store-main/")
def get_base_page(request: Request, param: int = 0):
    print(param)
    return templates.TemplateResponse("store.html", {"request": request})


@router.get("/comparison/")
def get_base_page(request: Request):
    return templates.TemplateResponse("comparison.html", {"request": request})


@router.get("/catalog/")
def get_base_page(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request})


@router.get("/basket/")
def get_base_page(request: Request):
    return templates.TemplateResponse("basket.html", {"request": request})


@router.get("/register/")
def get_base_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})