from dataclasses import dataclass

from domain.pokemon import Pokemon


@dataclass(frozen=True)
class UserSummary:
    id: int
    username: str
    pokemon_ids: list[int]


@dataclass(frozen=True)
class UserProfile:
    id: int
    username: str
    email: str
    pokemons: list[Pokemon]