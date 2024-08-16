from pydantic import Field, BaseModel
from pydantic.dataclasses import dataclass
from enum import Enum, auto


class BotClassEnum(Enum):
    Warrior = auto()
    Cleric = auto()
    Paladin = auto()
    Ranger = auto()
    Shadowknight = auto()
    Druid = auto()
    Monk = auto()
    Bard = auto()
    Rogue = auto()
    Shaman = auto()
    Necromancer = auto()
    Wizard = auto()
    Magician = auto()
    Enchanter = auto()
    Beastlord = auto()
    Berserker = auto()


@dataclass
class Spell:
    is_detrimental: bool


class Bot(BaseModel):
    bot_class: BotClassEnum
    name: str = Field(min_length=3)
    gems: dict[int, list[Spell]] = Field(
        default_factory=lambda: {i: list() for i in range(1, 13)}
    )
