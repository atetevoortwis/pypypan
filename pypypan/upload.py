import logging
import pywikibot
from pathlib import Path
from excel import read_pattypan_input, CommonsItem

site = pywikibot.Site('commons:test')
def upload_image(item: CommonsItem):
    imagepage = pywikibot.FilePage(site, item.title) 
    imagepage.text = item.description
    try:
        site.upload(filepage=imagepage, source_filename=item.path,report_success=True,ignore_warnings=False)
    except Exception as e:
        logging.exception(e)

def upload_pattypan_excel(filename: Path):
    items = read_pattypan_input(filename)
    for item in items:
        upload_image(item)
