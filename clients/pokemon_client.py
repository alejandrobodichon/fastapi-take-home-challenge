import asyncio
from collections.abc import Iterable

import httpx
from pydantic import BaseModel, ValidationError

from core.exceptions import PokemonApiUnavailable, PokemonNotFound
from domain.pokemon import Pokemon


class _PokemonResponse(BaseModel):
    id: int
    name: str

    def to_domain(self) -> Pokemon:
        return Pokemon(
            id = self.id,
            name= self.name
        )


class PokemonClient:
    def __init__(self, http: httpx.AsyncClient):
        self._http = http

    async def get_pokemon(self, id: int) -> Pokemon:
        try:
            response = await self._http.get(f"/pokemon/{id}")
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise PokemonNotFound() from e
            raise PokemonApiUnavailable() from e 
        except httpx.RequestError as e:
            raise PokemonApiUnavailable() from e

        try:
            return _PokemonResponse.model_validate(response.json()).to_domain()
        except ValidationError as e:
            raise PokemonApiUnavailable() from e 

        
    async def get_many(self, pokemon_ids: Iterable[int]) -> dict[int, Pokemon]:
        unique_ids = set(pokemon_ids)
        results = await asyncio.gather(*(self.get_pokemon(pid) for pid in unique_ids))
        return {p.id: p for p in results}
    