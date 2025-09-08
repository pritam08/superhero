import os, sys
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.mongodb import db
from app.models.user import UserIn, UserOut, UserInDB
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/register', response_model=UserOut)
async def register(user_in: UserIn):
    exists =  db.users.find_one({'username': user_in.username})
    if exists:
        raise HTTPException(status_code=400, detail='username already exists')
    hashed = get_password_hash(user_in.password)
    user = {
    'username': user_in.username,
    'hashed_password': hashed,
    'favorites': [],
    'role': 'user'
    }
    res =  db.users.insert_one(user)
    return { 'id': str(res.inserted_id), 'username': user_in.username, 'favorites': [], 'role': 'user' }


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.users.find_one({'username': form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    if not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access_token = create_access_token(subject=str(user['_id']), expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return { 'access_token': access_token, 'token_type': 'bearer' }