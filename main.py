from pdf_extraction_project import extract_pdf_content, save_to_json

if __name__ == "__main__":
    pdf_path = "data/1. Gioi thieu chung.pdf"  # Đường dẫn file PDF
    output_file = "cleaned_content.json"

    # Trích xuất nội dung PDF
    segments = extract_pdf_content(pdf_path)
    if segments:
        save_to_json(output_file, segments)
    else:
        print("Không có nội dung để lưu.")
