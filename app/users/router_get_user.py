from fastapi import APIRouter, Depends, Response

from app.exceptions import (IncorrectEmailOrPasswordException,
                            UserAlreadyExistsException)
from app.users.auth import (authenticate_user, 
                            create_access_token,
                            get_password_hash
                            )
from app.users.DAO import UsersDAO
from app.users.dependencies import get_admin_user, get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.get("/me")
async def read_users_me(user: Users = Depends(get_current_user)):
    return user
    
@router.get("/all")
async def read_users_all(user: Users = Depends(get_admin_user)):
    return await UsersDAO.find_all()
    
