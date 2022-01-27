import logging
import pywikibot
from pathlib import Path
from pypypan.excel import read_pattypan_input, CommonsItem

site = pywikibot.Site('commons:commons')
test_site = pywikibot.Site('commons:test')


def upload_image(item: CommonsItem, site: pywikibot.Site, update_existing: bool = False) -> False:
    imagepage = pywikibot.FilePage(site, item.title)
    imagepage.text = item.description
    try:
        if imagepage.exists():
            logging.error("File {} exists on {}".format(
                item.path.name, str(site)))
            if update_existing:
                logging.info(f"Updating description of {item.path.name}")
                imagepage.save("update")
                return True
            else:
                return False
        return site.upload(filepage=imagepage, source_filename=item.path, report_success=False)

    except Exception as e:
        logging.exception(e)
        raise e


def upload_pattypan_excel(filename: Path, update_existing: bool = False, max_uploads: int = -1, use_test_commons: bool = True):
    try:
        items = read_pattypan_input(filename)
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
        if upload_image(item, update_existing=update_existing, site=site):
            n = n+1
        else:
            logging.error(f"Failed uploading {item.title} / {item.path.name}")
        if n >= max_uploads:
            return
