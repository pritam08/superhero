import os, sys
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.db.sqlite_db import UserDatabase
from app.core.security import decode_token


router = APIRouter(prefix='/users', tags=['users'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')
    username = payload.get('sub')
    user = UserDatabase.find_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    return user


@router.get('/me')
async def me(user: dict = Depends(get_current_user)):
    return { 'id': str(user['id']), 'username': user['username'], 'favorites': user.get('favorites', []), 'role': user.get('role', 'user') }


@router.post('/favorites/{hero_id}')
async def add_favorite(hero_id: int, user: dict = Depends(get_current_user)):
    if hero_id in user.get('favorites', []):
        raise HTTPException(status_code=400, detail='already in favorites')
    
    # Add to favorites list
    favorites = user.get('favorites', [])
    favorites.append(hero_id)
    UserDatabase.update_user_favorites(user['username'], favorites)
    return {'ok': True}


@router.delete('/favorites/{hero_id}')
async def remove_favorite(hero_id: int, user: dict = Depends(get_current_user)):
    # Remove from favorites list
    favorites = user.get('favorites', [])
    if hero_id in favorites:
        favorites.remove(hero_id)
    UserDatabase.update_user_favorites(user['username'], favorites)
    return {'ok': True}


@router.get('/favorites')
async def list_favorites(user: dict = Depends(get_current_user)):
    from app.db.sqlite_db import SuperheroDatabase
    
    favs = user.get('favorites', [])
    heroes = []
    for hero_id in favs:
        hero = SuperheroDatabase.find_hero_by_id(hero_id)
        if hero:
            heroes.append(hero)
    return heroes