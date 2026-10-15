"""seed demo data

Revision ID: 747e5ab568a9
Revises: 21a1f8721f87
Create Date: 2026-10-15 16:35:47.552393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import UTC, datetime



# revision identifiers, used by Alembic.
revision: str = '747e5ab568a9'
down_revision: Union[str, Sequence[str], None] = '21a1f8721f87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEMO_PASSWORD_HASH = "$argon2id$..."

DEMO_USERS = {
    "ash": [25, 1, 7],
    "misty": [120, 121, 54],
    "brock": [74, 95],
}

users = sa.table(
    "users",
    sa.column("username", sa.String),
    sa.column("email", sa.String),
    sa.column("password_hash", sa.String),
)
user_pokemons = sa.table(
    "user_pokemons",
    sa.column("user_id", sa.Integer),
    sa.column("pokemon_id", sa.Integer),
    sa.column("modified", sa.DateTime),
)


def upgrade() -> None:
    op.bulk_insert(
        users,
        [
            {"username": name, "email": f"{name}@example.com", "password_hash": DEMO_PASSWORD_HASH}
            for name in DEMO_USERS
        ],
    )

    conn = op.get_bind()
    rows = conn.execute(
            sa.text("SELECT username, id FROM users WHERE username = ANY(:names)"),
            {"names": list(DEMO_USERS)},
        ).all()
    ids: dict[str, int] = {username: user_id for username, user_id in rows}

    op.bulk_insert(
        user_pokemons,
        [
            {"user_id": ids[name], "pokemon_id": pokemon_id, "modified": datetime.now(UTC)}
            for name, pokemon_ids in DEMO_USERS.items()
            for pokemon_id in pokemon_ids
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text("DELETE FROM users WHERE username = ANY(:names)").bindparams(
            names=list(DEMO_USERS)
        )
    )
