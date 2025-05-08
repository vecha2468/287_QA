import pandas as pd
import os


def initialize_output(output_dir, output_file):
    full_path = os.path.join(output_dir, output_file)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Check if the file exists and remove it if it does
    if os.path.exists(full_path):
        os.remove(full_path)

    # Return full path to be used with context manager later
    return full_path


def save_response(full_path, responses):
    # Using the context manager to handle the Excel file
    with pd.ExcelWriter(full_path, engine='xlsxwriter') as writer:
        df = pd.DataFrame(responses, columns=['Index', 'subkey', 'Response', 'expout'])  # Only store responses
        df.to_excel(writer, index=False, sheet_name='Results')


def finalize_output(writer):
    writer.close()