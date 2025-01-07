from fastapi import APIRouter, Request, Response
from fastapi.exceptions import HTTPException
from auth import check_user_authorize, get_id_from_access_token
from fastapi.templating import Jinja2Templates
from database import get_item_by_id, async_session, get_start_items, get_user_by_uid
from auth import check_user_authorize, get_id_from_access_token

router = APIRouter(
    tags=["pages"],
    prefix="/page",
)
templates = Jinja2Templates(directory="static")


@router.get("/store-main/")
async def get_base_page(request: Request, response: Response):
    v = {}
    n = 1
    tokens = await check_user_authorize(request=request, response=response)
    uid = await get_id_from_access_token(tokens.get("jwt_access_token"))
    user = await get_user_by_uid(async_session=async_session, id=uid)

    if not tokens:
        v['username'] = ''
    else:
        v['username'] = user.name

    v['request'] = request
    items = await get_start_items(async_session=async_session, c=4)
    for item in items:
        v[f'item_id_{n}'] = item.item_id
        v[f'title_{n}'] = item.fullname
        v[f'item_name_{n}'] = item.fullname
        v[f'item_url_{n}'] = item.img_url
        v[f'item_brand_{n}'] = item.brand
        v[f'item_price_{n}'] = item.price
        n += 1
    return templates.TemplateResponse("store.html", v)


@router.get("/comparison/")
async def get_base_page(request: Request):
    return templates.TemplateResponse("comparison.html", {"request": request})


@router.get("/user/")
async def get_base_page(request: Request, response: Response):
    tokens = await check_user_authorize(request=request, response=response)
    if tokens == 0:
        raise HTTPException(status_code=401, detail='user is not authorized')
    else:
        id = await get_id_from_access_token(tokens.get('jwt_access_token'))
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
