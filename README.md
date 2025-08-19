# 360-degree feedback software for the Government of India related News Stories in Regional Media using AI/ML

## Problem Statement ID
PSCS_35

## Organization
Ministry of Information and Broadcasting

## SDG Mapping
- SDG 4: Quality Education
- SDG 9: Industry, Innovation and Infrastructure

## Problem Description
The Government of India needs a smart system to automatically collect, organize, and analyze news related to its projects and actions from ~8,400 regional media outlets in multiple Indian languages. Current manual feedback is slow and lacks real-time capabilities. An AI/ML solution can provide sentiment analysis (positive, neutral, negative), real-time notifications for negative news, and electronic management of media clippings, including OCR for scanned documents.

## Objectives
- Build a feedback software for government-related news stories in regional media using AI/ML.
- Crawl and collect news articles from 200+ regional media websites in multiple Indian languages.
- Automatically classify each story as favorable, neutral, or not favorable.
- Alert government officials in real time for negative stories.
- Digitally store and tag scanned news clippings with OCR for easy search.
- Provide a dashboard for insights, trends, and reports.

## Planned Tech Stack
- Python, Jupyter notebooks
- Web scraping: Requests, BeautifulSoup
- Sentiment analysis: NLTK/TextBlob or VADER
- OCR: pytesseract
- Database: SQLite or MongoDB
- Dashboard: Streamlit or simple web UI

## Timeline (First 8 Weeks)
- Weeks 1–2: Literature survey, requirement gathering
- Week 3: Tech stack setup, sample demos (OCR/sentiment)
- Week 4–5: Data collection (sample news/articles/images)
- Week 6: Initial web scraper, continue data prep
- Week 7: Prototype dashboard wireframe
- Week 8: Review-1 submission

## How to Run Demos
- Ensure you have Python 3.x and install dependencies from `requirements.txt`
- For OCR demo: Run `python src/ocr_demo.py` to extract text from `data/sample_news.png`
- For sentiment demo: Run `python src/sentiment_demo.py` to analyze sentiment in `data/sample_news.txt`

## Team
- Student A (Roll No): Web scraping, Sentiment
- Student B (Roll No): OCR, Database
- Student C (Roll No): Dashboard, Documentation

## References
See [references.txt](references.txt)
