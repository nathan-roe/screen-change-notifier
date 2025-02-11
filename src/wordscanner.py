from PIL import Image
import pytesseract

class WordScanner:

    def scan(file_path):
        return pytesseract.image_to_string(Image.open(file_path))
