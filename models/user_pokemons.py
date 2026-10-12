from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class UserPokemons(Base):
    __tablename__ = "user_pokemons"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), 
        primary_key= True
    )
    pokemon_id: Mapped[int] = mapped_column(Integer, primary_key= True)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )