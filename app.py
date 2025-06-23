# filepath: combine_files_form/app.py
from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError
from docx import Document
import pandas as pd
from reportlab.pdfgen import canvas
import logging
from reportlab.lib.utils import simpleSplit

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 50 MB

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def convert_to_pdf(filepath):
    """Convert non-PDF files to PDF."""
    filename, ext = os.path.splitext(filepath)
    pdf_path = f"{filename}.pdf"
    if ext == ".docx":
        # Convert Word document to PDF
        doc = Document(filepath)
        pdf_path = f"{filename}.pdf"
        doc.save(pdf_path)
    elif ext in [".xls", ".xlsx"]:
        # Convert Excel file to PDF
        pdf_path = f"{filename}.pdf"
        df = pd.read_excel(filepath)

        # Create a PDF canvas
        c = canvas.Canvas(pdf_path, pagesize=(11 * 72, 8.5 * 72))  # Landscape orientation (11x8.5 inches)
        width, height = 11 * 72, 8.5 * 72  # Page size in points

        # Set margins
        margin = 40
        x_start = margin
        y_start = height - margin

        # Calculate column widths and row heights
        col_width = (width - 2 * margin) / len(df.columns)
        row_height = 20  # Fixed row height

        # Draw the header row
        c.setFont("Helvetica-Bold", 10)
        for i, col in enumerate(df.columns):
            x = x_start + i * col_width
            c.drawString(x, y_start, str(col))

        # Draw the data rows
        c.setFont("Helvetica", 9)
        y = y_start - row_height
        for _, row in df.iterrows():
            for i, cell in enumerate(row):
                x = x_start + i * col_width
                # Wrap text if it overflows the column width
                wrapped_text = simpleSplit(str(cell), "Helvetica", 12, col_width)
                for line in wrapped_text:
                    c.drawString(x, y, line)
                    y -= 12  # Line height
                y += 12  # Adjust back after the last line
            y -= row_height
            if y < margin:  # Start a new page if the content exceeds the page height
                c.showPage()
                c.setFont("Helvetica", 9)
                y = y_start
        c.save()
    return pdf_path

def merge_pdfs(pdf_paths, output_path, password=None):
    """Merge PDFs and add a password."""

    merger = PdfMerger()
    for pdf in pdf_paths:
        try:
            # Validate the PDF before appending
            PdfReader(pdf)
            merger.append(pdf)
        except PdfReadError:
            print(f"Skipping invalid PDF: {pdf}")
            continue  # Skip invalid PDFs

    merger.write(output_path)
    merger.close()

    # Add password to the final PDF
    writer = PdfWriter()
    reader = PdfReader(output_path)
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(user_password="", owner_password=password, permissions_flag=3)
    with open(output_path, "wb") as f:
        writer.write(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    print("FILES RECEIVED:", request.files)
    print("FILES KEYS:", request.files.keys())

    files = request.files.getlist('pdf_files')
    password = request.form.get('pdf_password') or os.environ.get('PDF_PASSWORD', 'default_password')
    pdf_paths = []

    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if filename.endswith('.pdf'):
            # Validate the PDF
            try:
                PdfReader(filepath)
                pdf_paths.append(filepath)
            except PdfReadError as e:
                logger.error(f"Error reading {filename}: {e}")
                os.remove(filepath)  # Remove invalid PDF
                continue  # Skip invalid PDFs
        else:
            pdf_path = convert_to_pdf(filepath)
            pdf_paths.append(pdf_path)

    if not pdf_paths:
        return f"Error: No valid files to process. Received: {[f.filename for f in files]}", 400

    output_pdf = os.path.join(app.config['PROCESSED_FOLDER'], 'combined.pdf')
    merge_pdfs(pdf_paths, output_pdf, password)

    # Cleanup merged PDFs (except the final combined file)
    for pdf in pdf_paths:
        if os.path.exists(pdf) and pdf != output_pdf:
            os.remove(pdf)

    return render_template('result.html', download_link=output_pdf)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

@app.errorhandler(413)
def request_entity_too_large(error):
    return "Error - Please refresh the page and try again. File sizes cannot exceed 100 MB total.", 413

@app.errorhandler(500)
def internal_server_error(error):
    return "Error - Please refresh the page and try again. If the issue persists, contact support.", 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='127.0.0.1', port=port)