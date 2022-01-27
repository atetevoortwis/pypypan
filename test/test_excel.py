from pypypan import excel
from helper_functions import generate_random_image
import pytest
import pathlib
BASE_PATH = pathlib.Path(__file__).parent


@pytest.fixture
def prepare_test_data():
    # Generate random images for the ./data/data_test.xls
    generate_random_image(BASE_PATH / "./data/test1.jpg")
    generate_random_image(BASE_PATH / "./data/test2.jpg")


def test_read_valid_excel(prepare_test_data):
    data = excel.read_pattypan_input(BASE_PATH / "./data/data_test.xls")
    assert len(data) == 2


def test_read_not_existing_excel():
    with pytest.raises(FileNotFoundError):
        excel.read_pattypan_input(BASE_PATH / "./data/data_testabc.xls")
