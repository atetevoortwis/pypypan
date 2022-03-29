from pypypan import upload
from helper_functions import generate_random_image
import pathlib
import pywikibot
import pytest
from PIL import Image
BASE_PATH = pathlib.Path(__file__).parent


@pytest.fixture
def prepare_test_data():
    # Generate random images for the ./data/data_test.xls
    generate_random_image(BASE_PATH / "./data/testhash.jpg")


def test_phash():
    img = BASE_PATH / "data" / "rick.jpeg"
    img_small = BASE_PATH / "data" / "rick_small.jpg"
    hash = upload.phash_image(img)

    i = Image.open(img)
    w, h = i.size
    i = i.resize((int(w/5), int(h/5)))
    i.save(img_small)
    hash_small = upload.phash_image(img_small)
    assert hash == hash_small == 'e9c7326904cb996d'


def test_sha1hash():
    img = BASE_PATH / "data" / "rick.jpeg"
    hash = upload.sha1hash_image(img)
    assert hash == '6cd2868974b189e9dd94655bd3ef5b09374a2a44'


def test_check_if_image_exists(prepare_test_data):
    exists, name = upload.check_if_image_exists(
        BASE_PATH / "data" / "honda.jpeg")
    assert exists is True
    assert name == '2019_Honda_Jazz_1.5_E_(21).jpg'
    exists, name = upload.check_if_image_exists(
        BASE_PATH / "./data/testhash.jpg")
    assert exists is False
    assert name is None


def test_upload_same_hash():
    item = upload.CommonsItem(
        title="new honda", description="desc", path=BASE_PATH / "data" / "honda.jpeg")
    site = pywikibot.Site('commons:test')
    res = upload.upload_image(item=item, site=site,
                              update_existing=False, dry_run=True)
    assert res is False


def test_upload_new_file(prepare_test_data):
    item = upload.CommonsItem(
        title="new random", description="desc", path=BASE_PATH / "./data/testhash.jpg")
    site = pywikibot.Site('commons:test')
    res = upload.upload_image(item=item, site=site,
                              update_existing=False, dry_run=True)
    assert res is True
