def worksheet_exists(file_path, sheet_name):
    """Function to determine if a worksheet exists"""

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