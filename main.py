import sys
import os
import re
import fitz
import json
import tempfile
from PySide6 import QtCore, QtWidgets
from enum import Enum

class GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Saver")
        self.text = QtWidgets.QLabel(
            "Welcome!\nClick here to save all images from the selected PDFs.",
            alignment=QtCore.Qt.AlignCenter
        )
        self.filename = QtWidgets.QLabel("No files selected.", alignment=QtCore.Qt.AlignCenter)
        
        self.file_button = QtWidgets.QPushButton("Select Files")
        self.file_button.clicked.connect(self.open_FileDialog)
        
        self.scan_button = QtWidgets.QPushButton("Get Images!")
        self.scan_button.clicked.connect(self.grab_images)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.filename)
        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.scan_button)

    def unique_name(self, base_path):
        """Return a unique filename if base_path already exists."""
        counter = 1
        path, ext = os.path.splitext(base_path)
        candidate = base_path
        while os.path.exists(candidate):
            candidate = f"{path}_{counter}{ext}"
            counter += 1
        return candidate

    def sanitize_filename(self, name, max_length=150):
        """Replace illegal filename characters and truncate safely."""
        safe = re.sub(r'[\\/*?:"<>|]', "_", name)
        return safe[:max_length]
        
    
    def open_FileDialog(self):
        """Opens file selection dialog for multiple pdfs."""
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select File(s)", "", "*.pdf")
        if file_paths:
            self.file_paths = file_paths
            filenames = "\n".join(Path(fp).name for fp in file_paths)
            self.filename.setText(f"Selected Files:\n{filenames}")

    def grab_images(self):
        try:
            save_dir = os.path.abspath("attached_images")
            os.makedirs(save_dir, exist_ok=True)

            for pdf in self.file_paths:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                    attachment.SaveAsFile(tmpfile.name)
                    temp_pdf_path = tmpfile.name
    
                pdf = fitz.open(temp_pdf_path)
                for page_index in range(len(pdf)):
                    page = pdf.load_page(page_index)
                    image_list = page.get_images(full=True)
    
                    if image_list:
                        print(f"[+] Found {len(image_list)} images on page {page_index}")
                    else:
                        print(f"[!] No images found on page {page_index}")
    
                    for image_index, img in enumerate(image_list, start=1):
                        xref = img[0]
                        base_image = pdf.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
    
                        image_name = os.path.join(
                            save_dir,
                            f"{subject}_{page_index+1}_{image_index}.{image_ext}"
                        )
                        image_name = self.uniquename(image_name)
                        with open(image_name, "wb") as image_file:
                            image_file.write(image_bytes)
    
                        print(f"[+] Extracted image saved as {image_name}")
                        saved_any = True
    
                pdf.close()
                os.remove(temp_pdf_path)  # cleanup

            if saved_any:
                self.text.setText("Images saved!")
            else:
                self.text.setText("No image attachments found.")

        except Exception as e:
            self.text.setText(f"Error: {str(e)}")
            print(f"Exception occurred: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = GUI()
    widget.resize(400, 250)
    widget.show()
    sys.exit(app.exec())
