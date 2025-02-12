import os
import json
import re
from PyPDF2 import PdfReader

def extract_pdf_content(pdf_path):
    """Trích xuất nội dung từ file PDF và tối ưu bố cục."""
    if not os.path.exists(pdf_path):
        print(f"Tệp không tồn tại: {pdf_path}")
        return []

    segments = []
    try:
        reader = PdfReader(pdf_path)
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text:
                clean_text = clean_and_format_text(text)
                segments.append({"page": page_number, "content": clean_text})
    except Exception as e:
        print(f"Lỗi khi đọc PDF: {e}")
    return segments

def clean_and_format_text(text):
    """Làm sạch văn bản, sửa lỗi khoảng cách và tối ưu xuống dòng."""
    # Xóa khoảng trắng thừa và ký tự không cần thiết
    text = re.sub(r'\s+', ' ', text).strip()

    # Sửa lỗi chữ bị tách rời (VD: "H O C V I E N" -> "HOC VIEN")
    text = re.sub(r'(?<=\b[A-Z]) (?=[A-Z]\b)', '', text)

    # Loại bỏ URL lặp lại
    text = re.sub(r'www\.\S+', '', text)

    # Định dạng xuống dòng sau dấu câu
    text = re.sub(r'([.!?])\s+', r'\1\n\n', text)
    
    # Định dạng xuống dòng trong danh sách số và dấu gạch đầu dòng
    text = re.sub(r'(?<=\d)\.\s+', '.\n', text)
    text = re.sub(r'(?<=▪)\s+', '\n', text)
    
    return text.strip()

def save_to_json(output_path, data):
    """Lưu dữ liệu vào file JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Dữ liệu đã được lưu vào '{output_path}'.")

def save_to_txt(output_path, data):
    """Lưu dữ liệu vào file TXT để hiển thị dễ đọc hơn."""
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in data:
            f.write(f"Trang {segment['page']}:\n{segment['content']}\n\n" + "-"*40 + "\n\n")
    print(f"Dữ liệu đã được lưu vào '{output_path}'.")

if __name__ == "__main__":
    pdf_path = "data/1. Gioi thieu chung.pdf"  
    output_json = "cleaned_content.json"
    output_txt = "cleaned_content.txt"

    segments = extract_pdf_content(pdf_path)
    if segments:
        save_to_json(output_json, segments)
        save_to_txt(output_txt, segments)
    else:
        print("Không có nội dung để lưu.")