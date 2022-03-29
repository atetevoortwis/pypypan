import logging
import pywikibot
from pathlib import Path
from pypypan.excel import read_pattypan_input, CommonsItem
import requests
import hashlib

site = pywikibot.Site('commons:commons')
test_site = pywikibot.Site('commons:test')


def sanitize_title(title: str) -> str:
    # Remove double apostrophes: https://commons.wikimedia.org/wiki/MediaWiki:Titleblacklist-custom-double-apostrophe
    return title.replace("''", "'")

def phash_image(filename: Path) -> str:
    from PIL import Image
    import imagehash
    return str(imagehash.phash(Image.open(filename)))
    
def sha1hash_image(filename: Path) -> str:
    BLOCK_SIZE = 65536 # The size of each read from the file

    file_hash = hashlib.sha1() 
    with open(filename, 'rb') as f: 
        fb = f.read(BLOCK_SIZE) 
        while len(fb) > 0: 
            file_hash.update(fb) 
            fb = f.read(BLOCK_SIZE)
    return str(file_hash.hexdigest())

def check_if_image_exists(filename: Path):
    # First check the SHA1 hash
    hash = sha1hash_image(filename)
    o = requests.get("https://commons.wikimedia.org//w/api.php?action=query&format=json&list=allimages&aisha1={}".format(hash)).json()

    try:
        if len(o['query']['allimages']) > 0:
            return True,o['query']['allimages'][0]['name']
        else:
            return False,None
    except:
        return False,None


def upload_image(item: CommonsItem, site: pywikibot.Site, update_existing: bool = False, dry_run: bool = False) -> False:
    imagepage = pywikibot.FilePage(site, sanitize_title(item.title))
    imagepage.text = item.description
    try:
        # First, check if an imagepage with this title exists
        if imagepage.exists():
            if update_existing:
                logging.info(f"Updating description of {item.path.name}")
                if not dry_run:
                    imagepage.save("update")
                return True
            else:
                logging.info("File {} exists on {}, updating".format(
                    item.path.name, str(site)))
                return False
        else:
            if dry_run:
                return True
            else:
                # check if the image (hash based) already exists
                exists, name = check_if_image_exists(item.path)
                if exists:
                    logging.info("Skipping upload of {} since a file with the same SHA1 hash exists: {}".format(item.title,name))
                return site.upload(filepage=imagepage, source_filename=item.path, ignore_warnings=True)

    except Exception as e:
        logging.exception(e)
        raise e


def upload_pattypan_excel(filename: Path, update_existing: bool = False, max_uploads: int = -1,
                          use_test_commons: bool = True, dry_run: bool = False, allow_missing_files: bool = False):
    try:
        items = read_pattypan_input(filename, allow_missing_files=allow_missing_files)
    except Exception as e:
        logging.error(e)
        return
    if use_test_commons:
        site = pywikibot.Site('commons:test')
    else:
        site = pywikibot.Site('commons:commons')
    n = 0
    for item in items:
        logging.info(f"Uploading {item.title} to {site}")
        if upload_image(item, update_existing=update_existing, site=site, dry_run=dry_run):
            n = n+1
        else:
            logging.error(f"Failed uploading {item.title} / {item.path.name}")
        if n >= max_uploads and max_uploads > 0:
            logging.info(
                "Did {} out of {} maximum uploads".format(n, max_uploads))
            return
