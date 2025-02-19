import pdfplumber
import re
from difflib import unified_diff

def preprocess_text(text):
    # Define substitutions to normalize interchangeable terms or standardize common formats
    substitutions = {
        'Tender No. 23-002': 'Contract No. 23-002',
    }
    for old, new in substitutions.items():
        text = text.replace(old, new)
    return text

def extract_text_by_sections(path):
    sections = {}
    text = ''
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'  # Append text with new lines to separate pages clearly

    text = preprocess_text(text)  # Preprocess to remove standard differences

    # Improved regex to capture section titles more reliably
    section_pattern = re.compile(r'(?:\n|^)(\d+\.\d+(?:\.\d+)?\s+[^\n]+)(?:\n|$)')
    parts = section_pattern.split(text)

    for i in range(1, len(parts), 2):
        section_number = parts[i].strip()
        section_content = parts[i + 1].strip()
        sections[section_number] = section_content

    return sections

def compare_sections(sections1, sections2):
    all_sections = sorted(set(sections1.keys()).union(sections2.keys()))
    for section in all_sections:
        text1 = sections1.get(section, None)
        text2 = sections2.get(section, None)
        if text1 and not text2:
            print(f"Section {section} is missing in document 2.")
        elif text2 and not text1:
            print(f"Section {section} is missing in document 1.")
        elif text1 and text2:
            print(f"Comparing Section {section}:")
            diff = unified_diff(text1.splitlines(), text2.splitlines(), lineterm='', fromfile='document1', tofile='document2')
            diff_output = list(diff)
            if diff_output:
                print('\n'.join(diff_output))
            else:
                print("No differences.")
        print("\n" + "-"*40 + "\n")

# Example paths to your PDF files
path1 = 'Document1.pdf'
path2 = 'Document2.pdf'

# Extract sections from both documents
sections1 = extract_text_by_sections(path1)
sections2 = extract_text_by_sections(path2)

# Compare the sections
compare_sections(sections1, sections2)
