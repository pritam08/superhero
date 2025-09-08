import os, sys
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.db.mongodb import db
from bson import ObjectId
from app.core.security import decode_token


router = APIRouter(prefix='/users', tags=['users'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')
    user_id = payload.get('sub')
    user =  db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    return user


@router.get('/me')
async def me(user: dict = Depends(get_current_user)):
    return { 'id': str(user['_id']), 'username': user['username'], 'favorites': user.get('favorites', []), 'role': user.get('role', 'user') }


@router.post('/favorites/{hero_id}')
async def add_favorite(hero_id: int, user: dict = Depends(get_current_user)):
    if hero_id in user.get('favorites', []):
        raise HTTPException(status_code=400, detail='already in favorites')
    db.users.update_one({'_id': user['_id']}, {'$push': {'favorites': hero_id}})
    return {'ok': True}


@router.delete('/favorites/{hero_id}')
async def remove_favorite(hero_id: int, user: dict = Depends(get_current_user)):
    db.users.update_one({'_id': user['_id']}, {'$pull': {'favorites': hero_id}})
    return {'ok': True}


@router.get('/favorites')
async def list_favorites(user: dict = Depends(get_current_user)):
    favs = user.get('favorites', [])
    heroes = []
    for h in favs:
        hero =  db.superheroes.find_one({'id': h}, {'_id': 0})
        if hero:
            heroes.append(hero)
    return heroes