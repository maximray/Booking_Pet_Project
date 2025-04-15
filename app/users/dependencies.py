from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import Setting
from app.exceptions import (IncorrectFormatTokenException,
                            TokenAbsentException, TokenExpireException,
                            UserIsNotPresentException)
from app.users.DAO import UsersDAO
from app.users.models import Users


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token



async def get_current_user(token: str = Depends(get_token)):
    try: 
        payload = jwt.decode(
            token, Setting.SECRET_KEY, Setting.ALG
        )
    except JWTError:
        raise IncorrectFormatTokenException
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpireException
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    
    return user


async def get_admin_user(user: Users = Depends(get_current_user)):
    return user
