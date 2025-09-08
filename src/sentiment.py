
!pip install kaggle transformers pandas --quiet

from google.colab import files

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d kazanova/sentiment140 --unzip


import pandas as pd

df = pd.read_csv('training.1600000.processed.noemoticon.csv', encoding='latin-1', 
                 names=['sentiment', 'id', 'date', 'query', 'user', 'text'])

print(f"Total rows in dataset: {len(df)}")

df_sample = df.sample(1000, random_state=42).reset_index(drop=True)

from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def get_sentiment_action(label):
    if label in ['4 stars', '5 stars']:
        return "Positive", "✅ No action needed"
    elif label in ['1 star', '2 stars']:
        return "Negative", "⚠️ Action required"
    else:
        return "Neutral", "ℹ️ Monitor only"

results = []
for text in df_sample['text']:
    result = sentiment_pipeline(text)[0]
    sentiment, action = get_sentiment_action(result['label'])
    results.append({
        'text': text,
        'sentiment': sentiment,
        'score': result['score'],
        'action': action
    })

result_df = pd.DataFrame(results)
print(result_df.head())

result_df.to_csv("sentiment140_sample_results.csv", index=False, encoding="utf-8-sig")
print("✅ Results saved to sentiment140_sample_results.csv")
