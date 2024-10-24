import streamlit as st
import os
import re
from typing import Dict, Any
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
import openai

# Set up PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

# Set up OpenAI API
openai.api_key = "your-openai-key"

def rule_based_extraction(text: str) -> Dict[str, Any]:
    rules = {
        'brand_name': r'([\w\s]+(?:LONDON|INDIA|USA|CORP|INC|LTD))',
        'product_name': r'([\w\s]+(?:SHAMPOO|SOAP|CREAM|LOTION|DEODORANT|OIL|DEO))',
        'pack_size': r'(\d+(?:\.\d+)?\s*(?:ML|L|G|KG|OZ|FLOZ))',
        'mrp': r'MRP.*?(\d+(?:\.\d+)?)',
        'batch_number': r'(?:BATCH|LOT)[\s.:]*([A-Za-z0-9.-]+)',
        'manufacturing_date': r'(?:MFG|MFD|MANUFACTURING DATE)[\s.:](\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\w{3}\s\d{2,4})',
        'expiry_date': r'(?:EXP|EXPIRY|USE BEFORE|BEST BEFORE)[\s.:](\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\w{3}\s\d{2,4})',
        'date_range': r'(\d{2}[-/]\d{2}[-/]\d{2,4})\s*[-—]\s*(\d{2}[-/]\d{2}[-/]\d{2,4})',
    }
    results = {}
    for key, pattern in rules.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            if key == 'date_range':
                results['manufacturing_date'] = matches[0][0]
                results['expiry_date'] = matches[0][1]
            else:
                results[key] = matches[0]
        else:
            results[key] = "Not found"
    # Additional info extraction
    additional_info = re.findall(r'(?:WARNING|CAUTION|INGREDIENTS|DIRECTIONS):.*', text, re.IGNORECASE)
    results['additional_info'] = ' '.join(additional_info) if additional_info else "Not found"
    return results

# Prompt template for OpenAI
prompt_template = """
You are an advanced AI system trained on millions of product labels from various industries. Analyze the following text extracted from a product label and the results from rule-based extraction. Provide the most accurate information for each field, considering all possible variations and formats. Include a confidence score (0-100) for each answer.

Text from label: {text}

Rule-based extraction results: {rule_based_results}

For each field, provide your analysis in this format:
Field: [Your answer] (Confidence: [0-100])

Fields to analyze:

1. Brand name:
- Consider well-known brands and local/regional brands
- Look for words like "by", "from", or company names
- Brand names might be in all caps or title case
- Consider multi-word brand names (e.g., "Procter & Gamble", "Johnson & Johnson")

2. Product name:
- Can include product type, variant, or flavor
- Look for descriptive words like "premium", "organic", "natural"
- Consider multiple-word product names
- May include numbers or special characters

3. Pack size:
- Look for various units: ml, L, g, kg, oz, fl oz, etc.
- Consider terms like "Net Weight", "Net Content", "Volume", "Size"
- May be presented as single unit or multiple (e.g., "6 x 330ml")
- Could be in different number formats (e.g., 1,000 ml or 1000 ml)

4. MRP (Maximum Retail Price):
- Look for various currency symbols: ₹, $, €, £, etc.
- Consider terms like "MRP", "Price", "MSRP", "RRP"
- May include tax information (e.g., "inclusive of all taxes")
- Could be presented in different formats (e.g., 1,000.00 or 1000.00)

5. Batch number:
- May start with "Batch No.", "Lot No.", "B.", "L.", or similar
- Could be alphanumeric
- Might include special characters or be entirely numeric

6. Manufacturing date:
- Look for "Mfg Date", "Manufacturing Date", "Prod Date", "Made On", etc.
- Consider all possible date formats: DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD, DD-MM-YYYY, etc.
- Might be presented as month and year only (MM/YYYY)
- Could use abbreviated month names (e.g., Jan, Feb, Mar)

7. Expiry date or "Use before" date:
- Look for "Exp Date", "Use Before", "Best Before", "Use By", etc.
- Consider all possible date formats, including:
  DDMMYY, DDMMMYY, DDMMYYYY, DDMMMYYYY, YYYYMM, YYYYMMDD, YYMMDD, MMDD, MMYYYY, MMMYYYY, MMMDDY, MMMDDY
- Examples: 291023, 29OCT23, 29102023, 29OCT2023, 202310, 20231029, 231029, 1029, 102023, OCT2023, OCT2923, OCT292023
- Be aware that dates might be presented as a range (e.g., "03/24-02/27" where the first date is manufacturing and the second is expiry)
- For date ranges, always extract the later date as the expiry date
- May be presented as a duration from manufacturing (e.g., "Use within 12 months of manufacturing")
- Could be presented as season and year (e.g., "Spring 2025")
- For two-digit years, assume 20XX for years less than the current year, and 19XX otherwise
- If only month and year are given, assume the last day of the month
- Be prepared to handle unconventional formats and use logical deduction when necessary

8. Additional info:
- Look for ingredients list, usage instructions, warnings, storage information
- Consider regulatory information (e.g., FDA approval, CE marking)
- Look for contact information, website, or customer service numbers
- Consider information about the product's origin or place of manufacture

Provide your analysis for each field, ensuring you've considered all possible variations and formats. If you're unsure about any information, state it clearly and provide your reasoning.
"""

def analyze_with_openai(text, rule_based_results):
    # Combine text and rule-based results into the message format for chat models
    prompt = prompt_template.format(text=text, rule_based_results=str(rule_based_results))
    
    # Use OpenAI Chat API to get a response
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use the chat-based model like gpt-4 or gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are an AI specialized in product label analysis."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048,
        temperature=0
    )
    
    return response['choices'][0]['message']['content'].strip()


def process_image(image):
    try:
        # Perform OCR
        result = ocr.ocr(np.array(image), cls=True)
        extracted_text = ' '.join([line[1][0] for line in result[0]])
        # Perform rule-based extraction
        rule_based_results = rule_based_extraction(extracted_text)
        # Use OpenAI for advanced analysis
        openai_result = analyze_with_openai(extracted_text, rule_based_results)
        return openai_result
    except Exception as e:
        return f"Error processing image: {str(e)}"

# Streamlit UI
st.title("Advanced Product Label Information Extractor")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.write("Processing...")
        result = process_image(image)
        st.subheader("Extracted Information:")
        st.text(result)
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.write("Note: This application uses advanced techniques to extract product information from labels.")
