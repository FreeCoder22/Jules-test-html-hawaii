import docx

def read_docx_content(file_path):
    """Reads and prints the content of a .docx file."""
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    content = read_docx_content("Contenus site Hawaii.docx")
    print(content)