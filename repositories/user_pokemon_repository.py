from collections import defaultdict

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_pokemons import UserPokemons


class UserPokemonRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_many(self, user_id: int, pokemon_ids: list[int]):
        stmt = (
            insert(UserPokemons)
            .values([{"user_id": user_id, "pokemon_id": pid} for pid in pokemon_ids])
            .on_conflict_do_nothing()    
        )
        await self._session.execute(stmt)
        await self._session.commit()


    async def list_pokemons_ids(self, user_id:int) -> list[int]:
        stmt = (
            select(UserPokemons.pokemon_id)
            .where(UserPokemons.user_id == user_id)
            .order_by(UserPokemons.modified)    
        )
        result = await self._session.execute(stmt)
        return list(result.scalars())

    async def ids_by_user(self, user_ids: list[int]) -> dict[int, list[int]]:
        result = await self._session.execute(
            select(UserPokemons.user_id, UserPokemons.pokemon_id)
            .where(UserPokemons.user_id.in_(user_ids))
            .order_by(UserPokemons.modified)  
        )

        grouped: dict[int, list[int]] = defaultdict(list)
        for user_id, pokemon_id in result:
            grouped[user_id].append(pokemon_id)

        return grouped

    async def remove(self, user_id, pokemon_id: int) -> None:
        await self._session.execute(
            delete(UserPokemons).where(
                UserPokemons.user_id == user_id, 
                UserPokemons.pokemon_id == pokemon_id
            )
        )
        await self._session.commit()
