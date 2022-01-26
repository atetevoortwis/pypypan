from pypypan import excel
import pytest
import pathlib
BASE_PATH = pathlib.Path(__file__).parent


def test_read_valid_excel():
    data = excel.read_pattypan_input(BASE_PATH / "./data/data_test.xls")
    assert len(data) == 2


def test_read_not_existing_excel():
    with pytest.raises(FileNotFoundError):
        excel.read_pattypan_input(BASE_PATH / "./data/data_testabc.xls")
