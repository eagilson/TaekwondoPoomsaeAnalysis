import pandas as pd
from typing import Any

def worksheet_exists(file_path: str, sheet_name: str) -> bool:
    """
    Function to determine if a worksheet exists.
    
    Args:
        file_path (str): The path to the .xlsx file, including the file name.
        sheet_name (str): The sheet name to check in the file_path file.
        
    Returns:
        sheet_exists (bool): True if the sheet exists in the file. False if there is any error.
    """
    from pathlib import Path
    import pandas as pd

    # Check if file exists and is an Excel file
    file_path = Path(file_path).resolve()  # Normalize path
    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        return False
    
    if file_path.suffix.lower() not in ('.xlsx', '.xlsm'):
        print(f"Error: File '{file_path}' is not a supported Excel file (.xlsx or .xlsm).")
        return False
    
    try:
        # Load the Excel file with pandas
        excel_file = pd.ExcelFile(file_path)
        # Check if the sheet exists
        return sheet_name in excel_file.sheet_names
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def insert_contiguous_columns(
    df: pd.DataFrame,
    loc: int,
    column_names: list[str],
    fill_value: str | dict[str, Any] = ''
) -> pd.DataFrame:
    """
    Insert multiple contiguous columns at a specific position.
    
    Parameters
    ----------
    df : DataFrame
        Your scoring data (from PoomsaePro.db).
    loc : int
        Column position where the new block should start.
    column_names : list[str]
        Names of the new contiguous columns to insert.
    fill_value : str or dict, default ''
        - If str: same value is used for every new column.
        - If dict: per-column defaults. Any column not present in the dict
          falls back to ''.
    
    Returns
    -------
    DataFrame with the new columns inserted at `loc`.
    """
    if not column_names:
        return df

    if isinstance(fill_value, dict):
        data = {col: fill_value.get(col, '') for col in column_names}
        new_cols = pd.DataFrame(data, index=df.index)
    else:
        new_cols = pd.DataFrame(fill_value, index=df.index, columns=column_names)

    return pd.concat(
        [df.iloc[:, :loc], new_cols, df.iloc[:, loc:]],
        axis=1
    )