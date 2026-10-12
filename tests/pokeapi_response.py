POKEAPI_RESPONSES = {
    "1": {
        "id": 1, "name": "bulbasaur"
    },
    "25": {
        "id": 25, "name": "pikachu"
    }
}


def fake_pokemon(pokemon_id: int) -> dict:
    return {
        "id": pokemon_id,
        "name": f"pokemon_{pokemon_id}"
    }