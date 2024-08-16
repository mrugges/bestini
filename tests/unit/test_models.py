from bestini.models import Bot, BotClassEnum, Bot, Spell
from hypothesis import strategies as st, given
from icecream import ic
from tests.strategies import st_printable_text


class TestModels:
    @given(bot=st.builds(Bot, name=st_printable_text))
    def test_bot(self, bot):
        ic(bot)
