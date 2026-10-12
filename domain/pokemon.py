from dataclasses import dataclass

 
@dataclass(frozen=True)
class Pokemon:
    id: int
    name: str
