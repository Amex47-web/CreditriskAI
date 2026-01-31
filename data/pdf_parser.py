from pypdf import PdfReader
import os
from typing import List

class PDFParser:
    def __init__(self):
        pass

    def extract_text(self, file_path: str) -> str:
        """
        Extract full text from a PDF file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            reader = PdfReader(file_path)
            text = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
            
            return "\n".join(text)
        except Exception as e:
            print(f"Error parsing PDF {file_path}: {e}")
            return ""

    def save_text(self, text: str, output_path: str):
        """
        Save extracted text to a .txt file.
        """
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

if __name__ == "__main__":
    # Example usage (assuming a dummy pdf exists)
    parser = PDFParser()
    # print(parser.extract_text("example_report.pdf"))
