# Combine Files Application

This application allows users to upload multiple files (PDF, Word, Excel), convert them to PDFs if necessary, merge them into a single PDF, and optionally password-protect the final document. It is built using Python and Flask.

---

## Features

- Upload multiple files (PDF, Word, Excel).
- Convert Word and Excel files to PDF format.
- Merge multiple PDFs into a single document.
- Password-protect the final PDF to restrict editing.
- User-friendly interface with file upload and progress indication.

---

## Requirements

Before running the application, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/combine-files-app.git
   cd combine-files-app

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    
## Configuration
To set the password for the combined PDF, create a .env file in the root of the project with the following content:
    ```bash
    PDF_PASSWORD=your_secure_password

Alternatively, you can set the PDF_PASSWORD environment variable directly in your system.

## Usage
Start the Flask application:
    ```bash
    python app.py

Open your browser and navigate to:
http://127.0.0.1:5000

Upload your files, and the application will process them into a single password-protected PDF.

## Deployment
Deploying to Azure App Service
1. Install the Azure CLI: Azure CLI Installation Guide
2. Log in to Azure:
    ```bash
    az login
3. Create an Azure App Service and deploy the application:
    ```bash
    az webapp up --name combine-files-app --resource-group <resource-group> --runtime "PYTHON:3.8"
4. Set the PDF_PASSWORD environment variable in Azure:
    ```bash
    az webapp config appsettings set --name combine-files-app --resource-group <resource-group> --settings PDF_PASSWORD=your_secure_password

##Testing
1. Run the application locally and test with various file types and sizes.
2. Ensure the combined PDF is generated correctly and is password-protected.
3. Verify that the application handles invalid files gracefully.

##Troubleshooting
Common Issues
File Size Exceeds Limit: Ensure the total file size does not exceed 100 MB. You can adjust this limit in app.py:
• File Size Exceeds Limit: Ensure the total file size does not exceed 100 MB. You can adjust this limit in app.py:
    ```bash
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB
• Access Denied (403): Ensure the app is running on 0.0.0.0 for external access:
    ```bash
    app.run(debug=True, host='0.0.0.0', port=5000)

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Flask - Web framework used for this project.
PyPDF2 - Library for PDF manipulation.
ReportLab - Library for generating PDFs.