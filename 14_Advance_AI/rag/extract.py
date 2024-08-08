from pypdf import PdfReader

def pdf_text_extractor(filepath : str) -> None:
    content = ""
    print("PDF filepath : ",filepath)
    pdf_reader = PdfReader(filepath,strict=True)
    print(".......Extracting Texts from PDF........")
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            content += f"{page_text}\n\n"
    
    with open(filepath.replace("pdf","txt"), "w" ) as file:
        file.write(content)

    print("...Text File write Success....")


        