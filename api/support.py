from fastapi import APIRouter, Request, Response, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import check_user_authorize, get_id_from_access_token
import database

router = APIRouter(
    prefix="/sup",
    tags=["support"]
)


@router.post("/basket/add/")
async def add_item_to_basket(
        item: database.SItemAddToBasket, request: Request, response: Response,
):
    if not await check_user_authorize(request=request, response=response):
        raise HTTPException(status_code=401, detail='unauthorized')

    uid = await get_id_from_access_token(request.cookies.get('jwt_access_token'))
    item_add = database.BasketAddItem(user_id=uid, item_id=item.item_id)
    string_id = await database.add_item_to_basket(
        async_session=database.async_session,
        item=item_add
    )
    return string_id
