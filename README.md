# PDF Image Extractor

A lightweight Python utility for extracting images from PDF files.

## Features

- Open a PDF document
- Locate embedded images
- Export each image to its own file
- Save output into a chosen folder

## Installation

1. Clone this repository.
2. Create a virtual environment.
3. Install the required dependencies.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python extract_images.py input.pdf output_directory
```

Replace `input.pdf` with the PDF file you want to process and `output_directory` with the folder where the extracted images should be saved.

## Project Structure

- `extract_images.py` - main script for extracting images
- `requirements.txt` - Python dependencies
- `README.md` - project documentation

## Notes

This project is intended to make it easy to pull images out of PDF documents for reuse, inspection, or archival purposes.

## License

This project is provided as-is for personal and educational use.
