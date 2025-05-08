import pandas as pd
import json


def read_questions(file_path: str):
    # Load the data
    df = pd.read_excel(file_path)

    # Ensure that we're working on a copy of the slice to prevent SettingWithCopyWarning
    filtered = df[['subkey', 'input', 'contextDict', 'expoutput']].copy()

    # Safely convert JSON strings to dictionaries
    filtered['contextDict'] = filtered['contextDict'].apply(
        lambda x: json.loads(x.replace("'", "\"")) if isinstance(x, str) else {})
    filtered['expoutput'] = filtered['expoutput'].apply(
        lambda x: json.loads(x.replace("'", "\"")) if isinstance(x, str) else {})

    # Update 'contextDict' with a new entry (corrected approach)
    filtered['contextDict'] = filtered['contextDict'].apply(lambda d: {**d, 'State': 'New'})

    return filtered