import os, sys
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.sqlite_db import UserDatabase
from app.models.user import UserIn, UserOut, UserInDB
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/register', response_model=UserOut)
async def register(user_in: UserIn):
    exists = UserDatabase.find_user_by_username(user_in.username)
    if exists:
        raise HTTPException(status_code=400, detail='username already exists')
    hashed = get_password_hash(user_in.password)
    
    user = UserDatabase.create_user(user_in.username, hashed)
    if not user:
        raise HTTPException(status_code=400, detail='Failed to create user')
    
    return { 'id': str(user['id']), 'username': user_in.username, 'favorites': [], 'role': 'user' }


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print("---------------------")
    print(form_data)
    user = UserDatabase.find_user_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    if not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access_token = create_access_token(subject=user['username'], expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return { 'access_token': access_token, 'token_type': 'bearer' }