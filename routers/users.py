from fastapi import APIRouter, status

from dependencies import UserServiceDep
from schemas.user import UserCreate, UserPrivate, UserProfileResponse, UserUpdate
from schemas.pokemon import PokemonAdd

router = APIRouter()


@router.get("", response_model = list[UserProfileResponse])
async def get_users(service: UserServiceDep):
    return await service.list_users()

@router.post("", response_model= UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, service: UserServiceDep):
    return await service.create(user)

@router.get("/{user_id}", response_model= UserProfileResponse)
async def get_user(user_id: int, service: UserServiceDep):
    return await service.get_profile(user_id)

@router.patch("/{user_id}", response_model= UserPrivate)
async def update_user(user_id: int, data: UserUpdate, service: UserServiceDep):
    return await service.update(user_id, data)

@router.delete("/{user_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserServiceDep):
    return await service.delete(user_id)

@router.post("/{user_id}/pokemons", response_model= UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def add_user_pokemons(user_id: int, data: PokemonAdd, service: UserServiceDep):
    return await service.add_pokemons(user_id, data.pokemon_ids)

