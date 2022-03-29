from pathlib import Path
from pypypan.upload import upload_pattypan_excel
from pypypan.excel import read_pattypan_input, generate_pattypan_excel
import typer
import pywikibot  # noqa: F401
import logging


# TODO: Cleanup logging, put in config
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger("main")
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
# create file handler which logs even debug messages
fh = logging.FileHandler('pypypan.log')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
logging.getLogger().addHandler(fh)

stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
logging.getLogger().addHandler(stdout_handler)

logger.setLevel(logging.DEBUG)
logging.getLogger("pywiki").setLevel(logging.ERROR)
app = typer.Typer()


@app.command()
def upload(excel_file: Path, update_existing: bool = False, dry_run: bool = False,
           test_one: bool = False, use_test_commons: bool = False, allow_missing_files: bool = False):
    """
    Upload an excel file that is filled according to the Pattypan format.
    """
    if test_one:
        upload_pattypan_excel(excel_file, update_existing=update_existing, max_uploads=1,
                              allow_missing_files=allow_missing_files, use_test_commons=use_test_commons, dry_run=dry_run)
    else:
        upload_pattypan_excel(excel_file, update_existing=update_existing,
                              allow_missing_files=allow_missing_files, use_test_commons=use_test_commons, dry_run=dry_run)


@app.command()
def generate_excel(excel_file: Path = Path("./data.xls"), image_dir: Path = Path(".")):
    """
    Generate an excel file that is filled according to the Pattypan format.
    image_dir points to a directory containing the images to use.
    """
    if excel_file.exists():
        raise(FileExistsError(f"Excel file {excel_file} already exists"))

    generate_pattypan_excel(excel_file, image_dir)


@app.command()
def test_template(excel_file: Path):
    """
    Parse a template and use the first file to generate the description.
    For testing purposes, so files listed in the Excel are not checked for existence.
    """
    items = read_pattypan_input(excel_file, allow_missing_files=True)
    print(items[0].description)


@app.command()
def version():
    """
    Print the pypypan version number.
    Run pip3 install --upgrade pypypan to udpate.
    """
    import importlib.metadata
    print(importlib.metadata.version('pypypan'))

@app.callback()
def mainapp(verbose: bool = False):
    """
    Upload images to Wikimedia Commons from a simple Excel file.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Enabled verbose logging")

def main():
    app()

if __name__ == "__main__":
    main()
