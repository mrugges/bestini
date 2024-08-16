from string import printable
from hypothesis import strategies as st

st_printable_text = st.text(alphabet=printable, min_size=3)
