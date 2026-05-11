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
        self.scan_button = QtWidgets.QPushButton("Save!")
        self.scan_button.clicked.connect(self.grab)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.scan_button)

    def uniquename(self, base_path):
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
        
            
    def grabimages(self, mailbox, subfolder = None):
        MAILBOX_NAME = mailbox
        try:
            save_dir = os.path.abspath("attached_images")
            os.makedirs(save_dir, exist_ok=True)

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
