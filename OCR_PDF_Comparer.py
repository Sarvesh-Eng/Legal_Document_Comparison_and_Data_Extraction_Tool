# Required libraries
from pdf2image import convert_from_path
import pytesseract
import re
import pandas as pd

# Step 1: Convert PDF Pages to Images
def pdf_to_images(pdf_path, dpi=300):
    """
    Converts each page of a PDF into an image.
    Input:
        pdf_path: Path to the PDF file.
        dpi: Resolution of the converted images (higher DPI captures more detail).
    Output:
        List of images, each representing a page in the PDF.
    """
    images = convert_from_path(pdf_path, dpi=dpi)
    return images

# Step 2: Perform OCR on Images to Extract Text
def ocr_images(images):
    """
    Performs OCR on a list of images to extract text from each page.
    Input:
        images: List of images (one per PDF page).
    Output:
        List of text, each entry containing extracted text for a single page.
    """
    all_text = []
    for img in images:
        text = pytesseract.image_to_string(img)
        all_text.append(text)
    return all_text

# Step 3: Sort Text into Headers, Footers, Body, and Tables
def sort_text_by_sections(page_text, header_threshold=0.9, footer_threshold=0.1):
    """
    Categorizes text from each page into headers, footers, body content, and placeholders for tables.
    Input:
        page_text: Raw OCR text from a single page.
        header_threshold: Proportion of page height above which text is treated as a header.
        footer_threshold: Proportion of page height below which text is treated as a footer.
    Output:
        Dictionary with categorized text (headers, footers, body, tables).
    """
    headers, footers, body_content, tables = [], [], [], []
    for line in page_text.split('\n'):
        # Use regex to detect table patterns, e.g., lines with multiple columns or borders
        if re.match(r"(\|.*\|)", line):
            tables.append(line)
        elif re.match(r"\b(HEADER TEXT HERE)\b", line):  # Placeholder for real header regex
            headers.append(line)
        elif re.match(r"\b(FOOTER TEXT HERE)\b", line):  # Placeholder for real footer regex
            footers.append(line)
        else:
            body_content.append(line)

    return {"headers": headers, "footers": footers, "body": body_content, "tables": tables}

# Step 4: Process and Save to File
def process_pdf(pdf_path, output_path):
    """
    Full process to convert PDF to structured file with headers, footers, body, and tables.
    Input:
        pdf_path: Path to the PDF file.
        output_path: Path to save the final output file (CSV format).
    """
    # Convert PDF pages to images
    images = pdf_to_images(pdf_path)

    # Perform OCR on each page
    ocr_text = ocr_images(images)

    # Initialize list to hold sorted page data
    sorted_data = []

    # Process each page's OCR text to sort by sections
    for page_num, page_text in enumerate(ocr_text, start=1):
        sorted_page = sort_text_by_sections(page_text)
        sorted_page["page_num"] = page_num  # Add page number for reference
        sorted_data.append(sorted_page)

    # Convert to DataFrame for structured output
    df = pd.DataFrame(sorted_data)

    # Save to CSV file for easy viewing
    df.to_csv(output_path, index=False)

    print(f"Structured data saved to {output_path}")

# Example usage
pdf_path = "Document1.pdf"
output_path = "Output.csv"
process_pdf(pdf_path, output_path)
