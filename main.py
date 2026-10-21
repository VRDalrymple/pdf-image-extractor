import sys
import os
import re
import fitz
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog


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
            names = [os.path.basename(fp) for fp in file_paths]
            self.filename.setText("Selected Files:\n" + "\n".join(names))

    def grab_images(self):
        try:
            if not getattr(self, "file_paths", None):
                self.text.setText("Please select files first.")
                return

            save_dir = os.path.abspath("attached_images")
            os.makedirs(save_dir, exist_ok=True)
            saved_any = False

            for pdf_path in self.file_paths:
                doc = fitz.open(pdf_path)
                base_name = self.sanitize_filename(os.path.splitext(os.path.basename(pdf_path))[0])

                for page_index in range(len(doc)):
                    page = doc.load_page(page_index)
                    image_list = page.get_images(full=True)

                    if image_list:
                        print(f"[+] Found {len(image_list)} images on page {page_index}")
                    else:
                        print(f"[!] No images found on page {page_index}")

                    for image_index, img in enumerate(image_list, start=1):
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]

                        image_name = os.path.join(
                            save_dir,
                            f"{base_name}_{page_index + 1}_{image_index}.{image_ext}"
                        )
                        image_name = self.unique_name(image_name)
                        with open(image_name, "wb") as image_file:
                            image_file.write(image_bytes)

                        print(f"[+] Extracted image saved as {image_name}")
                        saved_any = True

                doc.close()

            if saved_any:
                self.text.setText("Images saved!")
            else:
                self.text.setText("No images found in the selected PDFs.")

        except Exception as e:
            self.text.setText(f"Error: {str(e)}")
            print(f"Exception occurred: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = GUI()
    widget.resize(400, 250)
    widget.show()
    sys.exit(app.exec())
