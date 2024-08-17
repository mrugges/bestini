from string import printable

from hypothesis import assume
from hypothesis import strategies as st
from icecream import ic

from bestini.models import Bot, Effect, EffectDirection, Spell, Stat

st_printable_text = st.text(alphabet=printable, min_size=3)

from collections import namedtuple

IntRange = namedtuple("IntRange", ["mn", "mx"])

st_file_path = st.text()


@st.composite
def st_int_range(draw) -> IntRange:
    mn = draw(st.integers(min_value=1, max_value=20000))
    mx = draw(st.integers(min_value=mn, max_value=20000))
    assume(mn <= mx)
    return IntRange(mn=mn, mx=mx)


@st.composite
def st_effect(draw, int_range=st_int_range()) -> Effect:
    effect_range = draw(int_range)
    return Effect(
        effect_direction=draw(st.sampled_from(EffectDirection)),
        effected_stat=draw(st.sampled_from(Stat)),
        min_value=effect_range.mn,
        max_value=effect_range.mx,
    )


st_spell = st.builds(Spell, effects=st.lists(st_effect()))

st_bot = st.builds(Bot, name=st_printable_text, spells=st.lists(st_spell))
