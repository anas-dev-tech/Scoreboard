import pdfplumber

file_path = "123.pdf"

def pdf_to_text():
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text
    
    
print(pdf_to_text())
