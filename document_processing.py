import os
from typing import Any
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx
from unstructured.partition.doc import partition_doc
from unstructured.partition.xlsx import partition_xlsx
from unstructured.partition.image import partition_image
from pydantic import BaseModel
from logging_config import get_logger
import pandas as pd

# Initialize logger
logger = get_logger()

class Element(BaseModel):
    type: str
    text: Any
    source: str

def xlsx_rows(path: str):
    rows = []
    df = pd.read_excel(path)
    for index, row in df.iterrows():
        # Convert the row to a string with columns separated by newlines
        row_string = '\n'.join(f"{col}: {row[col]}" for col in df.columns)
        rows.append(row_string)
    return rows

def partition_documents(path: str):
    elements = []
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        source = file_name
        logger.info(f"Starting partitioning {file_name}")
        try:
            if file_name.endswith('.pdf'):
                elements.extend([Element(type='pdf', text=str(el), source=source) for el in partition_pdf(file_path, languages=["eng", "deu"], strategy="hi_res", hi_res_model_name="yolox", pdf_infer_table_structure=True)])
            elif file_name.endswith('.docx'):
                elements.extend([Element(type='docx', text=str(el), source=source) for el in partition_docx(file_path)])
            elif file_name.endswith('.doc'):
                elements.extend([Element(type='doc', text=str(el), source=source) for el in partition_doc(file_path)])
            elif file_name.endswith('.xlsx'):
                elements.extend([Element(type='xlsx', text=str(el), source=source) for el in xlsx_rows(file_path)])
            elif file_name.endswith(('.jpg', '.jpeg', '.png')):
                elements.extend([Element(type='image', text=str(el), source=source) for el in partition_image(file_path, languages=["eng", "deu"], strategy="hi_res", hi_res_model_name="yolox", pdf_infer_table_structure=True)])
            else:
                logger.warning(f"Unsupported file format: {file_name}")
        except Exception as e:
            logger.error(f"Error partitioning {file_name}: {e}")
    logger.info("Finished partitioning documents.")
    return elements

def categorize_elements(raw_elements):
    logger.info("Starting categorizing documents...")
    categorized_elements = []
    try:
        for element in raw_elements:
            if "Table" in str(type(element)):
                categorized_elements.append(Element(type="table", text=element.text, source=element.source))
            else:
                categorized_elements.append(Element(type="text", text=element.text, source=element.source))
        logger.info("Finished categorizing documents.")
    except Exception as e:
        logger.error(f"Error categorizing documents: {e}")
    return categorized_elements

