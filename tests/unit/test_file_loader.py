from icecream import ic
from bestini.file_loader import FileLoader
from hypothesis import strategies as st, given
from tests.strategies import st_file_path


class TestFileLoader:

    def test_parse(self):
        FileLoader().parse()
