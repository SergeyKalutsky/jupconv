from PIL import Image
from fpdf import FPDF
from notebook_reader import NotebookParser

notebook_filepath = r"C:\Users\Skalutsky\data\JUPYTER NOTEBOOKS\CWORKS market.ipynb"
np = NotebookParser(notebook_filepath)
layout = np.create_layout()

pdf = FPDF()
pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)
pdf.add_page()


for element in layout:
    if element['content_type'] == 'text':
        text = element['content'][0].replace('#', '').strip()
        pdf.write(10, text)
        pdf.ln(10)

    if element['content_type'] == 'image':
        with Image.open(element['content']) as img:
            print(img.size[0]//5, img.size[1]//5)
            pdf.image(element['content'], w=img.size[0]//5, h=img.size[1]//5)
            pdf.ln(10)

pdf.output("unicode.pdf", 'F')
np.delete_temp_folder()