from pathlib import Path
import pandas as pd
from typing import List
from dataclasses import dataclass


@dataclass
class CommonsItem:
    title: str
    description: str
    path: Path


def read_pattypan_input(filename: Path) -> List[CommonsItem]:
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
        raise FileNotFoundError("File {filename} does not exist")

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
    except ValueError:
        raise ValueError(f"Cell A1 not found in {filename}")

    allowed_missing_columns = ['name', 'path']
    for col in data.columns:
        if f"${{{col}}}" not in tpl and col not in allowed_missing_columns:
            raise ValueError(f"Column {col} not used in template")

    items = []
    for i, row in data.iterrows():
        if not Path(row.path).exists:
            raise FileNotFoundError("File {filename} does not exist")
        tpl_values = {}
        for col in data.columns:
            if col in allowed_missing_columns:
                continue
            tpl_values[col] = row[col]
        items.append(CommonsItem(path=Path(row.path),
                                 description=tpl.replace(
                                     "${", "{").format(**tpl_values),
                                 title=row.name))
    return items
