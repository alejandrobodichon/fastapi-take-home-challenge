from typing import Annotated

import httpx
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from clients.pokemon_client import PokemonClient
from core.database import get_db
from repositories.user_pokemon_repository import UserPokemonRepository
from repositories.user_repository import UserRepository
from services.user_service import UserService


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

HttpClientDep = Annotated[httpx.AsyncClient, Depends(get_http_client)]

def get_user_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)

def get_user_pokemon_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> UserPokemonRepository:
    return UserPokemonRepository(db)

def get_pokemon_client(http: HttpClientDep) -> PokemonClient:
    return PokemonClient(http)

PokemonClientDep = Annotated[PokemonClient, Depends(get_pokemon_client)]

def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    user_pokemon_repo: Annotated[UserPokemonRepository, Depends(get_user_pokemon_repo)],
    pokemon_client: Annotated[PokemonClient, Depends(get_pokemon_client)],
) -> UserService:
    return UserService(repo, user_pokemon_repo, pokemon_client)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
