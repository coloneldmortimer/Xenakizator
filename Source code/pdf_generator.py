from fpdf import FPDF

def pdf_table_from_matrix(pdf, data, header=None):
    pdf.set_font("helvetica", size=10)

    line_height = 1.4 * pdf.font_size

    # Values normalization
    def norm(v):
        if isinstance(v, float):
            # 2 decimals
            return f"{v:.2f}"
        if isinstance(v, (list, tuple)):
            # lists
            return ", ".join(f"{x:.2f}" if isinstance(x, float) else str(x) for x in v)
        if v is None:
            return ""
        return str(v)

    rows = []
    if header:
        rows.append([norm(c) for c in header])
    rows += [[norm(c) for c in row] for row in data]

    ncols = max(len(r) for r in rows)
    col_width = pdf.epw / ncols
    col_widths = tuple(col_width for _ in range(ncols))

    # Adds the table to the pdf
    for row_data in rows:
        for cell in row_data:
            pdf.cell(col_width, line_height, cell, border=1)
        pdf.ln(line_height)

def generate_pdf(point, sect_tot, filename="tabella.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for sect in range(sect_tot):
        pdf.add_page()
        pdf.set_font("helvetica", size=12)

        # Section header
        pdf.cell(200, 10, f"Sezione {sect + 1}", ln=True, align="C")
        pdf.ln(5)  # Interlinea titolo e tabella

        # Datas for the section
        data = point[sect]

        # Table header
        header = ["Instanti t", "Classe timbrica", "Strumento", "Nota", "Durata", "Intensità", "Glissandi"]

        # Generates the section table
        pdf_table_from_matrix(pdf, data, header)

    # Saves pdf
    pdf.output(filename)