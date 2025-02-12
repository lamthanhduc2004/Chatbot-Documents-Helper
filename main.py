from extractor import extract_pdf_content, save_to_json

if __name__ == "__main__":
    pdf_path = "data/1. Gioi thieu chung.pdf"  # Thay bằng đường dẫn file PDF của bạn
    output_file = "bert_extracted_content.json"

    # Bước 1: Trích xuất nội dung PDF
    segments = extract_pdf_content(pdf_path)
    if segments:
        # Lưu kết quả trích xuất vào file JSON
        save_to_json(output_file, segments)
    else:
        print("Không có nội dung để lưu.")
