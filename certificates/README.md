# Certificates Folder

This folder should contain the PDF certificate files for each participant.

## File Naming Convention

For automatic certificate sending, name your PDF files using this format:
- `mprincerainier_certificate.pdf`
- `madelynadelaida_certificate.pdf`

## Manual Certificate Sending

You can also send certificates manually by specifying the full path to the PDF file when prompted by the email script.

## Supported File Types

- PDF files (.pdf) - Recommended for certificates
- Other document types are also supported

## Example Usage

1. Place your certificate PDFs in this folder
2. Run the email script: `python email_sender.py`
3. Choose option 2 for bulk certificate sending
4. The script will automatically match certificates to recipients based on email addresses
