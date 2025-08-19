import pytesseract
from PIL import Image


img = Image.open('sample_news.png')


text = pytesseract.image_to_string(img)


print("Extracted Text:\n", text)
