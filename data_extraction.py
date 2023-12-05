import fitz
import pandas as pd


def make_text(words):
    line_dict = {}
    words.sort(key=lambda w: w[0])
    for w in words:
        y1 = round(w[3], 1)
        word = w[4]
        line = line_dict.get(y1, [])
        line.append(word)
        line_dict[y1] = line
    lines = list(line_dict.items())
    lines.sort()
    return "\n".join([" ".join(line[1]) for line in lines])


def extract_data_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_annots = []

    for pageno in range(len(doc)):
        page = doc[pageno]
        words = page.get_text("words")

        for annot in page.annots():
            if annot is not None:
                rec = annot.rect
                mywords = [w for w in words if fitz.Rect(w[:4]) in rec]
                ann = make_text(mywords)
                all_annots.append(ann)

    return all_annots


def clean_and_process_data(all_annots):
    cont = [annot.split('\n', 1) for annot in all_annots]

    liss = []
    for i in range(len(cont)):
        lis = []
        for j in cont[i]:
            j = j.replace('*', '')
            j = j.replace('#', '')
            j = j.replace(':', '')
            j = j.strip()
            lis.append(j)
        liss.append(lis)

    keys = []
    values = []

    for i in liss:
        keys.append(i[0])
        values.append(i[1])

    for i in range(len(values)):
        for j in range(len(values[i])):
            if values[i][j] >= 'A' and values[i][j] <= 'Z':
                break
        if j == len(values[i]) - 1:
            values[i] = values[i].replace(' ', '')

    report = dict(zip(keys, values))
    report['VEHICLE IDENTIFICATION'] = report.get('VEHICLE IDENTIFICATION', '').replace(' ', '')

    dic = [report.get('LOCALITY', ''), report.get('MANNER OF CRASH COLLISION/IMPACT', ''), report.get('CRASH SEVERITY', '')]
    print(report.keys())

    val_after = []
    for local in dic:
        li = []
        lii = []
        k = ''
        extract = ''
        l = 0
        for i in range(len(local) - 1):
            if local and local[i + 1] >= '0' and local[i + 1] <= '9':
                li.append(local[l:i + 1])
                l = i + 1
        li.append(local[l:])
        for i in li:
            if i and i[0] in lii:
                k = i[0]
                break
            lii.append(i[0])
        for i in li:
            if i and i[0] == k:
                extract = i
                val_after.append(extract)
                break

    report['LOCALITY'] = val_after[0]
    report['MANNER OF CRASH COLLISION/IMPACT'] = val_after[1]
    report['CRASH SEVERITY'] = val_after[2]

    data = pd.DataFrame.from_dict(report)
    data.to_csv('final.csv', index=False)


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text()
    return text


if __name__ == "__main__":
    pdf_path = 'PDF/data-extraction-from-unstructured-pdfs.pdf'
    # all_annots = extract_data_from_pdf(pdf_path)
    # print(all_annots)
    # clean_and_process_data(all_annots)
    text = extract_text_from_pdf(pdf_path)
    print(text)
