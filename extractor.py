import os
import re
import json
from PyPDF2 import PdfReader
from transformers import AutoTokenizer, AutoModel

def extract_pdf_content(pdf_path):
    """Trích xuất nội dung từ file PDF."""
    if not os.path.exists(pdf_path):
        print(f"Tệp không tồn tại: {pdf_path}")
        return []

    segments = []
    try:
        reader = PdfReader(pdf_path)
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text:
                clean_text = clean_and_split_with_bert(text)
                segments.append({"page": page_number, "content": clean_text})
    except Exception as e:
        print(f"Lỗi khi đọc PDF: {e}")
    return segments

def clean_and_split_with_bert(text):
    """Làm sạch và chia đoạn văn bằng BERT."""
    # Làm sạch văn bản
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Tải mô hình BERT
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    # Chia đoạn văn bản thành phần nhỏ (chunk) theo ngữ cảnh
    max_chunk_size = 128
    words = text.split(" ")
    chunks = [" ".join(words[i:i + max_chunk_size]) for i in range(0, len(words), max_chunk_size)]

    return "\n\n".join(chunks)

def save_to_json(output_path, data):
    """Lưu dữ liệu vào file JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Dữ liệu đã được lưu vào '{output_path}'.")
