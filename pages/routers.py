from fastapi import APIRouter, Request, Response
from fastapi.exceptions import HTTPException
from auth import check_user_authorize, get_id_from_access_token
from fastapi.templating import Jinja2Templates
from database import get_item_by_id, async_session, get_start_items, get_user_by_uid


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
        "request": request, "item_url_1": item1.img_url, "title_1": item1.fullname, "item_brand_1": item1.brand, "item_name_1": item1.fullname, "item_price_1": item1.price,
        "item_url_2": item2.img_url, "title_2": item2.fullname, "item_brand_2": item2.brand, "item_name_2": item2.fullname, "item_price_2": item2.price,
        "item_url_3": item3.img_url, "title_3": item3.fullname, "item_brand_3": item3.brand, "item_name_3": item3.fullname, "item_price_3": item3.price,
        "item_id_1": item1.item_id, "item_id_2": item2.item_id, "item_id_3": item3.item_id,
    })


@router.get("/comparison/")
async def get_base_page(request: Request):
    return templates.TemplateResponse("comparison.html", {"request": request})


@router.get("/user/")
async def get_base_page(request: Request, response: Response):
    tokens = await check_user_authorize(request=request, response=response)
    if tokens == 0:
        raise HTTPException(status_code=401, detail='user is not authorized')
    elif tokens != 1:
        id = await get_id_from_access_token(tokens.get('jwt_access_token'))
    else:
        id = await get_id_from_access_token(request.cookies.get('jwt_access_token'))
    user = await get_user_by_uid(async_session=async_session, id=id)
    return templates.TemplateResponse("user.html", {
        "request": request, "username": user.name, "user_id": user.user_id,
        "user_is_superuser": user.is_superuser, "user_email": user.email
    })


@router.get("/catalog/")
async def get_base_page(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request})


@router.get("/basket/")
async def get_base_page(request: Request, response: Response):
    tokens = await check_user_authorize(request=request, response=response)
    if tokens == 0:
        raise HTTPException(status_code=401, detail='user is not authorized')
    elif tokens != 1:
        id = await get_id_from_access_token(tokens.get('jwt_access_token'))
    else:
        id = await get_id_from_access_token(request.cookies.get('jwt_access_token'))
    user = await get_user_by_uid(async_session=async_session, id=id)
    return templates.TemplateResponse("basket.html", {"request": request})


@router.get("/registration/")
async def get_base_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login/")
async def get_base_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
