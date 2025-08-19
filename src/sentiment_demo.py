from textblob import TextBlob


with open('sample_news.txt', 'r', encoding='utf-8') as f:
    samples = f.readlines()

for line in samples:
    blob = TextBlob(line)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    print(f"Text: {line.strip()}\nSentiment: {sentiment}\n")
