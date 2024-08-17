import string
from enum import StrEnum, auto
from typing import Optional, Self, Union

from pydantic import (
    BaseModel,
    Field,
    PositiveFloat,
    PositiveInt,
    field_validator,
    model_validator,
)
from pydantic.dataclasses import dataclass

from bestini.constants import MAX_LEVEL


class BotClass(StrEnum):
    Unknown = auto()
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


class BotRole(StrEnum):
    Tank = auto()
    Healer = auto()
    Important = auto()
    Unknown = auto()


class SpellType(StrEnum):
    Heal = auto()
    DamageOverTime = auto()
    DirectDamage = auto()
    HealOverTime = auto()
    DamageShield = auto()
    TargetAreaOfEffect = auto()
    PointBlankAreaOfEffect = auto()
    Buff = auto()


class SpellTarget(StrEnum):
    Single = auto()


class Skill(StrEnum):
    Alternation = auto()


class Stat(StrEnum):
    Health = auto()
    Strength = auto()
    Agility = auto()


class EffectDirection(StrEnum):
    Increase = auto()
    Decrease = auto()


class Effect(BaseModel):
    min_value: PositiveInt
    max_value: PositiveInt
    effect_direction: EffectDirection
    effected_stat: Stat

    @model_validator(mode="after")
    def check_range(self) -> Self:

        if self.min_value > self.max_value:
            raise ValueError("Effect min_value must be <= max_value")

        return self


Level = PositiveInt
LevelField = Field(ge=1, le=MAX_LEVEL, default=1)


class ClassLevelRequirement(BaseModel):
    bot_class: BotClass = BotClass.Unknown
    min_level: Level = LevelField


class Spell(BaseModel):
    spell_type: SpellType
    damage: PositiveInt
    heal: PositiveInt
    spell_range: PositiveInt
    cast_time: PositiveFloat
    recast_time: PositiveFloat
    recovery_time: PositiveFloat
    mana_cost: PositiveInt
    target: SpellTarget
    skill: Skill
    fades_message: str
    cast_on_you_message: str
    cast_on_other_message: str
    class_level_requirements: list[ClassLevelRequirement]
    effects: list[Effect]


class SpellAction(BaseModel):
    spell: Spell
    gem: int = Field(ge=1, le=12)


class OptherAction(BaseModel):
    action: str


class Section(BaseModel):
    options: dict[str, list[Union[SpellAction, OptherAction]]]


class BotIni(BaseModel):
    sections: dict[str, Section]
    file_path: str


class Bot(BaseModel):
    bot_class: BotClass = BotClass.Unknown
    name: str = Field(min_length=3)
    gems: dict[int, list[Spell]] = Field(
        default_factory=lambda: {i: list() for i in range(1, 13)}
    )
    level: Level = LevelField
    role: BotRole = BotRole.Unknown
    spells: list[Spell] = []
