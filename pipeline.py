import fitz
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text()
    return text


def identify_headers(text):
    doc = nlp(text)
    headers = [token.text for token in doc if token.is_title]
    return headers


def identify_lists(text):
    doc = nlp(text)
    lists = [sent.text for sent in doc.sents if sent.text.startswith(('*', '-', '•'))]
    return lists


def main():
    pdf_path = "PDF/Test PDF.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)

    headers = identify_headers(extracted_text)
    lists = identify_lists(extracted_text)
    print(extracted_text)
    print(headers)


if __name__ == '__main__':
    main()