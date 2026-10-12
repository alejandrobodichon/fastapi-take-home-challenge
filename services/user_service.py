from clients.pokemon_client import PokemonClient
from core.auth import hash_password
from core.exceptions import (
    EmailAlreadyExists,
    NotAuthorized,
    UsernameAlreadyExists,
    UserNotFound,
)
from domain.user_profile import UserProfile
from models.user import User
from repositories.user_pokemon_repository import UserPokemonRepository
from repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(
            self, 
            user_repo: UserRepository,
            user_pokemon_repo: UserPokemonRepository,
            pokemon_client: PokemonClient
    ):
        self._repo = user_repo
        self._user_pokemon_repo = user_pokemon_repo
        self._pokemon_client = pokemon_client

    async def create(self, user_create: UserCreate) -> User:
        if await self._repo.exist_by_email(user_create.email):
            raise EmailAlreadyExists()
        
        if await self._repo.exist_by_username(user_create.username):
            raise UsernameAlreadyExists()

        user = User(
            username = user_create.username,
            email = user_create.email,
            password_hash = hash_password(user_create.password)
        )

        return await self._repo.save(user= user)


    async def get(self, user_id: int) -> User:
        user = await self._repo.get_by_id(user_id)

        if user is None:
            raise UserNotFound()
    
        return user
        

    async def get_profile(self, user_id: int) -> UserProfile:
            user = await self._repo.get_by_id(user_id)
    
            if user is None:
                raise UserNotFound()
            
            pokemon_ids = await self._user_pokemon_repo.list_pokemons_ids(user_id)
            pokemons = await self._pokemon_client.get_many(pokemon_ids)
        
            return UserProfile(
                id = user.id,
                email= user.email,
                username=user.username,
                pokemons= [pokemons[id] for id in pokemon_ids]
            )


    async def list_users(self) -> list[UserProfile]:
        users = await self._repo.get_all()
        ids_by_user = await self._user_pokemon_repo.ids_by_user([u.id for u in users])

        all_ids = {pid for ids in ids_by_user.values() for pid in ids}
        pokemons = await self._pokemon_client.get_many(all_ids)

        return [
            UserProfile(id = user.id,
                        email= user.email,
                        username=user.username,
                        pokemons= [pokemons[id] for id in ids_by_user.get(user.id,[])])
            for user in users
        ]


    async def update(self, user_id: int, data: UserUpdate) -> User:
        user = await self.get(user_id)

        if data.email is not None and data.email != user.email:
            if await self._repo.exist_by_email(data.email):
                raise EmailAlreadyExists()
        if data.username is not None and data.username != user.username:
            if await self._repo.exist_by_username(data.username):
                raise UsernameAlreadyExists() 

        for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
            setattr(user, field, value)
        
        return await self._repo.save(user)

    async def delete(self, user_id: int) -> None:
        user = await self.get(user_id)
        await self._repo.delete(user)

    async def add_pokemons(self, user_id: int, pokemons_ids: list[int]):
        await self._pokemon_client.get_many(pokemons_ids)
        await self._user_pokemon_repo.add_many(user_id, pokemons_ids)
        return await self.get_profile(user_id)
