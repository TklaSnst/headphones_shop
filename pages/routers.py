from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from database import get_item_by_id, async_session, Item


router = APIRouter(
    tags=["pages"],
    prefix="/page",
)
templates = Jinja2Templates(directory="static")


@router.get("/store-main/")
async def get_base_page(request: Request, param: int = 0):
    item1 = await get_item_by_id(async_session=async_session, item_id=1)
    item2 = await get_item_by_id(async_session=async_session, item_id=2)
    item3 = await get_item_by_id(async_session=async_session, item_id=3)
    return templates.TemplateResponse("store.html", {
        "request": request, "item_url_1": item1.img_url, "title_1": item1.fullname, "item_brand_1": item1.brand, "item_name_1": item1.fullname,
        "item_url_2": item2.img_url, "title_2": item2.fullname, "item_brand_2": item2.brand, "item_name_2": item2.fullname,
        "item_url_3": item3.img_url, "title_3": item3.fullname, "item_brand_3": item3.brand, "item_name_3": item3.fullname,
    })


@router.get("/comparison/")
async def get_base_page(request: Request):
    return templates.TemplateResponse("comparison.html", {"request": request})


@router.get("/catalog/")
async def get_base_page(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request})


@router.get("/basket/")
async def get_base_page(request: Request):
    return templates.TemplateResponse("basket.html", {"request": request})


@router.get("/register/")
async def get_base_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})