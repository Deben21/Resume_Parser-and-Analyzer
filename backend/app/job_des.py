import spacy
import sys, fitz

model_path = r"C:\Users\thapa\OneDrive\Desktop\project dump\major_project-master v2.1\backend\JdModel\output\model-best"
jdnlp = spacy.load(model_path)

def extract_jdtext_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as pdf_document:
            
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text()

    except Exception as e:
        print(f"Error: {e}")

    return text

