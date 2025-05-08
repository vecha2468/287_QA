import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
import re
from tqdm import tqdm

# Ensure NLTK resources are downloaded
nltk.download('punkt')

# Define transportation modes for categorization with more inclusive regex patterns
category_keywords = {
    'Public': r'(\b(bus|train|local|subway|tram|metro|trolly|streetcar|light rail|commuter train|shuttle|minibus)\b|\bpublic\s+(transport|bus|transit))',
    'Private': r'(\b(car|motorcycle|scooter|bike|bicycle|motorbike|SUV|personal|sedan|coupe|electric scooter)\b|\bprivate\s+vehicle)',
    'Maritime': r'\b(boat|ship|ferry|yacht|sailboat|motorboat|canoe|kayak|cruise|water|sail)\b',
    'Aerospace': r'\b(airplane|jet|helicopter|aircraft|drone|glider|airliner|biplane|chopper|airbus)\b',
}

# Pre-compile regex patterns for efficiency
compiled_patterns = {category: re.compile(pattern, re.IGNORECASE) for category, pattern in category_keywords.items()}


def categorize_transportation(response):
    # Check if response is a string and is not NaN
    if pd.isna(response) or not isinstance(response, str):
        return {'Keyword match': '0', 'Category match': 'N/A'}

    response_cleaned = response.lower()
    found_categories = set()

    # Apply patterns to the entire cleaned response
    for category, pattern in compiled_patterns.items():
        if pattern.search(response_cleaned):
            found_categories.add(category)

    # Assume 'Multiple' for any detection of keywords, '0' if none found
    keyword_match = 'Multiple' if found_categories else '0'
    if(len(found_categories) == 1):
        keyword_match = '1'
    category_match = next(iter(found_categories), 'N/A')

    return {'Keyword Match': keyword_match, 'Category Match': category_match}

def process_responses(file_path):
    df = pd.read_excel(file_path)

    tqdm.pandas(desc="Processing Responses")
    df['aiout'] = df['Response'].progress_apply(categorize_transportation)

    df.to_excel(file_path.replace('.xlsx', '_updated.xlsx'), index=False)

# Path to the Excel file
file_path = 'output/test_output.xlsx'
process_responses(file_path)
