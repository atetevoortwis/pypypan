from pathlib import Path
import pandas as pd
from typing import List
from dataclasses import dataclass
import logging


@dataclass
class CommonsItem:
    title: str
    description: str
    path: Path


def generate_pattypan_excel(excel_file: Path, image_dir: Path):
    """
    Function that generates a Pattypan Excel file that contains the images from image_dir
    """
    pass


def read_pattypan_input(filename: Path, allow_missing_files: bool = False) -> List[CommonsItem]:
    """
    Reads an Excel file following the Pattypan format:
        (https://commons.wikimedia.org/wiki/Commons:Pattypan/Simple_manual)
    This should have two worksheets:
    - 'Template', containing a single cell A1 that holds the template used
      to generate the description for the Commons page
    - 'Data', containing rows with all items to upload.
      There are two mandatory columns:
        - name: the name (title) of the item
        - path: the path to the file to upload
      All other columns are optional and free to choose,
      but they should match a placeholder in the beforementioned template.
      E.g., a column 'creator' will be used to fill the ${creator} placeholder in the template

    The functions returns a list of CommonsItem objects,
    which hold a title, a description and a path to the file to upload.
    """
    if not filename.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    try:
        data = pd.read_excel(filename, sheet_name='Data')
    except ValueError:
        raise ValueError(f"Sheet 'Data' not found in {filename}")

    try:
        tpl = pd.read_excel(filename, sheet_name='Template')
    except ValueError:
        raise ValueError(f"Sheet 'Template' not found in {filename}")

    try:
        tpl = tpl.columns[0]
        # Replace brackets
        tpl = tpl.replace("{{", "{{{{")
        tpl = tpl.replace("}}", "}}}}")
    except ValueError:
        raise ValueError(f"Cell A1 not found in {filename}")

    allowed_missing_columns = ['name', 'path']
    for col in data.columns:
        if f"${{{col}}}" not in tpl and col not in allowed_missing_columns:
            raise ValueError(f"Column {col} not used in template")

    items = []
    for i, row in data.iterrows():
        """
        There are three options for the file path:
        - Absolute
        - Relative to Pattypan excel location
        - Relative to current working dir
        All of these are checked (in this order) and if one of them exists, it is used.
        """
        # TODO: check if this is ok
        # Convert backslashes to forward, since both POSIX and Windows handle the latter well
        rawpath = Path(row['path'].replace('\\', '/'))
        if rawpath.is_absolute():
            path = rawpath
        elif (filename.parent / rawpath).exists():
            path = filename.parent / rawpath
        elif (Path.cwd() / rawpath).exists():
            path = Path.cwd() / rawpath
        else:
            path = rawpath
        if not path.exists():
            if allow_missing_files:
                logging.error(f"File {row['path']} does not exist")
            else:
                raise FileNotFoundError(f"File {row['path']} does not exist")
        else:
            logging.debug("File exists: {}".format(path))

        tpl_values = {}
        for col in data.columns:
            if col in allowed_missing_columns:
                continue
            if col == 'category':
                # Special case: expand categories
                if ";" in row[col]:
                    categories = row[col].split(";")
                    tpl_values[col] = "]]\r\n[[Category:".join(categories)
                else:
                    tpl_values[col] = row[col]
            else:
                tpl_values[col] = row[col]
        items.append(CommonsItem(path=path,
                                 description=tpl.replace(
                                     "${", "{").format(**tpl_values),
                                 title=row['name']))
    return items
