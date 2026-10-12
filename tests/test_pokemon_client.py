from io import BytesIO
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from httpx import AsyncClient

from main import app
from tests.conftest import create_test_user


@pytest.mark.anyio
async def test_pokemon_add_when_server_down(client, pokeapi_overrides):
    user = await create_test_user(client)
    pokeapi_overrides["25"] = httpx.Response(500)

    response = await client.post(
        f"/users/{user["id"]}/pokemons",
        json={"pokemon_ids": [25]},
    )

    assert response.status_code == 502


@pytest.mark.anyio
async def test_pokemon_add_when_pokemon_doesnt_exist(client):
    user = await create_test_user(client)

    response = await client.post(
        f"/users/{user["id"]}/pokemons",
        json={"pokemon_ids": [1099]},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Pokemon not found."}
    profile = await client.get(f"/users/{user["id"]}")
    assert profile.json()["pokemons"] == []


@pytest.mark.anyio
async def test_pokemon_add_and_exist(client):
    user = await create_test_user(client)

    response = await client.post(
        f"/users/{user["id"]}/pokemons",
        json={"pokemon_ids": [25]},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": user["id"], "username": user["username"], "email": "test@example.com", "pokemons": [{"id": 25, "name": "pikachu"}]
    }


@pytest.mark.anyio
async def test_pokemon_add_and_exist_idempotence(client):
    user = await create_test_user(client)

    response = await client.post(
        f"/users/{user["id"]}/pokemons",
        json={"pokemon_ids": [25]},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": user["id"], "username": user["username"], "email": "test@example.com", "pokemons": [{"id": 25, "name": "pikachu"}]
    }

    response2 = await client.post(
            f"/users/{user["id"]}/pokemons",
            json={"pokemon_ids": [25]},
        )

    assert response2.status_code == 201
    assert response2.json() == {
            "id": user["id"], "username": user["username"], "email": "test@example.com", "pokemons": [{"id": 25, "name": "pikachu"}]
        }