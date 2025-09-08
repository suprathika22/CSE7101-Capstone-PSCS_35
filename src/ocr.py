!sudo apt install tesseract-ocr -y
!pip install pytesseract pillow textblob pandas

import pytesseract
from PIL import Image
from google.colab import files
from textblob import TextBlob
import pandas as pd

uploaded = files.upload()

results = []

for img_name in uploaded.keys():
    text = pytesseract.image_to_string(Image.open(img_name))
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0:
        sentiment = "Positive"
        action = "✅ No action needed"
    elif polarity < 0:
        sentiment = "Negative"
        action = "⚠️ Action required"
    else:
        sentiment = "Neutral"
        action = "ℹ️ Monitor only"
    
    results.append({
        "Image": img_name,
        "Extracted_Text": text.strip(),
        "Sentiment": sentiment,
        "Action": action
    })


df = pd.DataFrame(results)
df.to_csv("image_sentiments.csv", index=False, encoding="utf-8-sig")

print("✅ Results saved to image_sentiments.csv")
