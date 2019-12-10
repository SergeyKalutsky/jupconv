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
        pdf.write(8, text)
        pdf.ln(8)

pdf.output("unicode.pdf", 'F')