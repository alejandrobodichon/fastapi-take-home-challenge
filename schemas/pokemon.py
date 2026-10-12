from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

PokemonId = Annotated[int, Field(gt=0)]

class PokemonAdd(BaseModel):
    pokemon_ids: list[PokemonId] = Field(min_length=1, max_length=10)

class PokemonSummary(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
    