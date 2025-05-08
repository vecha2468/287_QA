import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import requests
from PIL import Image
from io import BytesIO

# Define the folders and their respective categories
folders = {
    'output_cheapest': 'Cheapest',
    'output_fastest': 'Fastest',
    'output_safest': 'Safest',
    'output_seasonally_preferable': 'Seasonally Preferable'
}


# Function to plot the result column
def plot_result_distribution(df, title, output_dir):
    result_counts = df['result'].value_counts()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Bar plot
    result_counts.plot(kind='bar', color=['skyblue', 'lightgreen', 'salmon'], ax=axes[0])
    axes[0].set_title(f'Result Distribution: {title}')
    axes[0].set_xlabel('Result')
    axes[0].set_ylabel('Frequency')
    axes[0].grid(axis='y')

    # Pie chart
    result_counts.plot(kind='pie', autopct='%1.1f%%', colors=['skyblue', 'lightgreen', 'salmon'], ax=axes[1])
    axes[1].set_title(f'Result Proportion: {title}')
    axes[1].set_ylabel('')

    plt.tight_layout()
    output_path = os.path.join(output_dir, f'{title}_combined.png')
    plt.savefig(output_path)
    plt.close()
    return output_path


# Function to plot stacked bar chart for comparative results
def plot_comparative_results(dfs, categories, output_dir):
    result_counts = {category: df['result'].value_counts() for category, df in dfs.items()}
    result_df = pd.DataFrame(result_counts).fillna(0)
    result_df.plot(kind='bar', stacked=True, figsize=(10, 6), color=['skyblue', 'lightgreen', 'salmon'])
    plt.title('Comparative Results')
    plt.xlabel('Result')
    plt.ylabel('Frequency')
    plt.xticks(rotation=0)
    plt.grid(axis='y')
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'comparative_results.png')
    plt.savefig(output_path)
    plt.close()
    return output_path


# Function to plot pass, fail, and partial percentages for each category
def plot_result_percentages(dfs, categories, output_dir):
    result_percentages = {category: df['result'].value_counts(normalize=True) * 100 for category, df in dfs.items()}
    result_percent_df = pd.DataFrame(result_percentages).fillna(0)
    result_percent_df.plot(kind='bar', figsize=(10, 6), color=['skyblue', 'lightgreen', 'salmon'])
    plt.title('Result Percentages by Category')
    plt.xlabel('Result')
    plt.ylabel('Percentage')
    plt.xticks(rotation=0)
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'result_percentages.png')
    plt.savefig(output_path)
    plt.close()
    return output_path


# Function to plot the proportion of test cases for each category
def plot_test_case_proportion(dfs, categories, output_dir):
    test_case_counts = {category: len(df) for category, df in dfs.items()}
    test_case_df = pd.Series(test_case_counts)
    test_case_df.plot(kind='pie', autopct='%1.1f%%', figsize=(10, 6),
                      colors=['skyblue', 'lightgreen', 'salmon', 'orange'])
    plt.title('Proportion of Test Cases by Category')
    plt.ylabel('')
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'test_case_proportion.png')
    plt.savefig(output_path)
    plt.close()
    return output_path


# Function to plot scores for each category
def plot_scores(dfs, categories, output_dir):
    score_data = {category: df['score'] for category, df in dfs.items()}
    score_df = pd.DataFrame(score_data)
    score_df.plot(kind='box', figsize=(10, 6))
    plt.title('Scores by Category')
    plt.xlabel('Category')
    plt.ylabel('Score')
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'scores.png')
    plt.savefig(output_path)
    plt.close()
    return output_path


# Function to create PDF with plots and descriptions
def create_pdf(image_paths, descriptions, summary_image_paths, summary_descriptions, pdf_filename, title_image_url):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add the title page
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.multi_cell(0, 10, "Testing Genie AI: transportation related queries", align='C')
    pdf.ln(10)

    # Download the image and add it to the title page
    response = requests.get(title_image_url)
    img = Image.open(BytesIO(response.content))
    img_path = 'title_image.png'
    img.save(img_path)
    pdf.image(img_path, x=10, y=pdf.get_y(), w=pdf.w - 2 * pdf.l_margin)

    # Add the detailed pages with combined plots and descriptions
    for image_path, description in zip(image_paths, descriptions):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, description)
        pdf.ln(10)
        pdf.image(image_path, x=10, y=pdf.get_y(), w=pdf.w - 2 * pdf.l_margin)

    # Add the summary page with smaller plots and descriptions
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "Summary of Results")
    pdf.ln(5)
    for image_path, description in zip(summary_image_paths, summary_descriptions):
        pdf.image(image_path, x=10, y=pdf.get_y(), w=90)
        pdf.ln(55)  # Move to the next line after image
        pdf.multi_cell(0, 10, description)
        pdf.ln(5)
    pdf.output(pdf_filename)


# Directory where the plots will be saved
output_dir = 'plots'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List to store image paths for the PDF
image_paths = []
summary_image_paths = []
# Dictionary to store dataframes for each category
dfs = {}

# Process each folder
for folder, category in folders.items():
    file_path = os.path.join(folder, 'test_output_results.xlsx')
    if os.path.exists(file_path):
        try:
            # Read the first sheet dynamically
            df = pd.read_excel(file_path, sheet_name=0)
            dfs[category] = df
            # Generate and save combined plots
            image_paths.append(plot_result_distribution(df, category, output_dir))
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

# Generate comparative results plot
if dfs:
    summary_image_paths.append(plot_comparative_results(dfs, folders.values(), output_dir))
    summary_image_paths.append(plot_result_percentages(dfs, folders.values(), output_dir))
    summary_image_paths.append(plot_test_case_proportion(dfs, folders.values(), output_dir))
    summary_image_paths.append(plot_scores(dfs, folders.values(), output_dir))

# Example descriptions for each plot
descriptions = [
    "These plots show the distribution and proportion of test results for the 'Cheapest' category.",
    "These plots show the distribution and proportion of test results for the 'Fastest' category.",
    "These plots show the distribution and proportion of test results for the 'Safest' category.",
    "These plots show the distribution and proportion of test results for the 'Seasonally Preferable' category."
]

summary_descriptions = [
    "This stacked bar chart shows a comparative view of the test results across all categories.",
    "This bar chart shows the pass, fail, and partial percentages for each category.",
    "This pie chart shows the proportion of test cases for each category.",
    "This box plot shows the distribution of scores for each category."
]

# URL of the title image
title_image_url = 'https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/8c/c7/68/8cc76883-a24a-664a-6d8a-177aeaf1021c/AppIcon-0-0-1x_U007epad-0-85-220.jpeg/1200x630wa.png'

# Create the PDF with plots and descriptions
pdf_filename = 'Test_Case_Results_Analysis.pdf'
create_pdf(image_paths, descriptions, summary_image_paths, summary_descriptions, pdf_filename, title_image_url)
