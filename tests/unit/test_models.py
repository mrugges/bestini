from hypothesis import given
from hypothesis import strategies as st
from icecream import ic

from bestini.constants import MAX_LEVEL
from bestini.models import Bot, BotClass, Effect, Spell
from tests.strategies import IntRange, st_bot, st_effect, st_int_range, st_spell


class TestModels:

    @given(int_range=st_int_range())
    def test_int_range(self, int_range: IntRange):
        assert int_range.mn <= int_range.mx

    @given(effect=st_effect())
    def test_effect(self, effect: Effect):
        assert effect.min_value <= effect.max_value

    @given(spell=st_spell)
    def test_spell(self, spell: Spell):
        for req in spell.class_level_requirements:
            assert req.min_level <= MAX_LEVEL
            assert req.min_level >= 0

    @given(bot=st_bot)
    def test_bot(self, bot):
        assert len(bot.name) >= 3
        assert len(bot.gems.keys()) == 12
