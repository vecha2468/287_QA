import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def safe_json_loads(s):
    try:
        # Replace single quotes with double quotes to correct the JSON formatting
        corrected_json = s.replace("'", '"')
        return json.loads(corrected_json.strip())  # Attempt to load the corrected JSON string
    except ValueError as e:
        print(f"JSON parsing error: {e} for JSON: {s}")  # Debugging output
        return {}  # Return empty dictionary if JSON is invalid

def compare(d1, d2):
    result=d1.get("Transportation Method", "").lower()
    print(d2,'checkinbg')
    d2_lower= d2.lower()
    if result in d2_lower:
        return 'pass'
    else:
        return 'fail'

def process_excel(file_path,visualization_path_file):
    df = pd.read_excel(file_path)
    print("DataFrame loaded:", df.head())  # Print the first few rows to verify content

    df['result'] = df.apply(lambda row: compare(safe_json_loads(row['expout']), row['Response']), axis=1)
    df['score'] = df['result'].map({'pass': 1,  'fail': 0})

    total_pass = (df['result'] == 'pass').sum()
    total_fail = (df['result'] == 'fail').sum()
    test_score = df['score'].sum()

    with PdfPages(visualization_path_file) as pdf:
        plt.figure(figsize=(8, 6))
        results = ['Pass', 'Fail']
        counts = [total_pass, total_fail]
        plt.bar(results, counts, color=['green', 'yellow', 'red'])
        plt.title('Test Results')
        plt.xlabel('Result Type')
        plt.ylabel('Count')
        plt.grid(True)
        pdf.savefig()
        plt.close()

        text_str = f"Total Passes: {total_pass}\nTotal Fails: {total_fail}\nTest Score: {test_score}"
        plt.figure(figsize=(8, 6))
        plt.text(0.01, 0.5, text_str, wrap=True)
        plt.axis('off')
        pdf.savefig()
        plt.close()

    output_path = file_path.replace('.xlsx', '_results.xlsx')
    df.to_excel(output_path, index=False)
    print(f"Done. Saved results to {output_path} and PDF to 'output/results_visualization.pdf'")
    print(f"Total Passes: {total_pass},  Total Fails: {total_fail}, Test Score: {test_score}")

    return df

# Example usage
file_path = 'output/test_output.xlsx'
visualization_path_file= 'output/results_visualization.pdf'
file_path_1='output/test_output_Deepseek.xlsx'
visualization_path_file_1= 'output/results_visualization_Deepseek.pdf'
df = process_excel(file_path,visualization_path_file)
df_1 = process_excel(file_path_1,visualization_path_file_1)