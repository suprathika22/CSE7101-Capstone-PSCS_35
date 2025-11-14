# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import pytesseract
from PIL import Image
from datetime import datetime

# --- CONFIGURATION ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
# NOTE: Set the correct path for Tesseract executable based on your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load departments configuration
try:
    with open('departments.json', 'r') as f:
        DEPARTMENTS_CONFIG = json.load(f)
except FileNotFoundError:
    print("ERROR: departments.json not found!")
    DEPARTMENTS_CONFIG = []

# Mock database for verified posts (Starts completely EMPTY as requested)
VERIFICATION_LOG = [] 

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- HELPER FUNCTIONS ---

def perform_ocr(image_path):
    """Performs OCR on an image file using Tesseract."""
    try:
        text = pytesseract.image_to_string(Image.open(image_path), lang='eng') 
        return text.strip(), "Image (OCR)"
    except Exception as e:
        print(f"OCR Error: {e}")
        return f"Error extracting text: {e}", "Image (OCR)"

def translate_to_english(text):
    """
    MOCK Placeholder for language translation (simulates translation to English)
    Includes specific logic for the Telugu Harassment sentence.
    """
    
    # Check for known Telugu harassment phrase
    if "వేధించిన అమ్మాయి" in text or "ఒక అబ్బాయి వేధించిన అమ్మాయి" in text:
        translated_text = "A girl was harassed by a boy."
        detected_lang = "Telugu"
        return translated_text, detected_lang
    
    # Mock fallback for other non-English text (assuming 'Hindi' for demonstration)
    if any(char > '\u0900' and char < '\u097f' for char in text): # Rough check for Devanagari/Indic script
        detected_lang = "Hindi/Other"
        translated_text = "[[Non-English Translation Mock]] The news mentions harassment or crime." # Use strong keywords
        return translated_text, detected_lang
        
    detected_lang = "English"
    return text, detected_lang

def classify_department(text):
    """Classifies the text into one or more government departments based on keywords."""
    text_lower = text.lower()
    found_departments = []
    
    for dept in DEPARTMENTS_CONFIG:
        for keyword in dept['keywords']:
            if keyword in text_lower:
                found_departments.append(dept['name'].capitalize())
                break
    
    return ", ".join(found_departments) if found_departments else "General"

def analyze_sentiment(text):
    """MOCK sentiment analysis function."""
    text_lower = text.lower()
    
    # Include harassment/crime keywords in the negative list for strong matching
    negative_words = [
        "harass", "abuse", "assault", "bad", "problem", "loss", 
        "crime", "theft", "murder", "election", 
        
        # Weather/Disaster (Existing/Updated)
        "storm", "flood", "cyclone", "disaster", "warning", "damage", 
        "drought", "closure", "heavy rain", "wind", "cold",
        
        # Agriculture Negative (Existing/Updated)
        "pest", "disease", "crop failure", "shortage", "protest", "deficit",
        
        # ENVIRONMENT NEGATIVE (NEW)
        "pollution", "emission", "climate change", "deforestation", "waste", "smog", "hazard", "toxic" 
    ]
    
    positive_words = ["good", "great", "excellent", "win", "achievement", "success", "profit", "holiday", "festival"]
    pos_count = sum(text_lower.count(word) for word in positive_words)
    neg_count = sum(text_lower.count(word) for word in negative_words)

    if pos_count > neg_count:
        sentiment = "Positive"
        polarity = 0.5
    elif neg_count > pos_count:
        sentiment = "Negative"
        polarity = 0.5
    else:
        sentiment = "Neutral"
        polarity = 0.0

    return sentiment, polarity 

def log_verification(snippet, sentiment, polarity, departments, source, lang):
    """Adds the verified post to the log."""
    existing_orders = [log['order'] for log in VERIFICATION_LOG]
    order = max(existing_orders) + 1 if existing_orders else 1
    
    hour = datetime.now().hour

    new_id = len(VERIFICATION_LOG) + 1
    
    VERIFICATION_LOG.append({
        'id': new_id,
        'snippet': snippet,
        'sentiment': sentiment,
        'polarity': polarity,
        'departments': departments,
        'time_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'source': source,
        'lang': lang,
        'order': order, 
        'time_of_day': hour
    })

# --- ROUTES ---

@app.route('/')
@app.route('/home')
@app.route('/verify')
def index():
    return render_template('index.html')

@app.route('/departments')
def departments():
    dept_stats = {}
    
    for log in VERIFICATION_LOG:
        for dept_name_raw in log['departments'].split(', '):
            dept_name = dept_name_raw.lower().strip()
            if dept_name == 'general' or not dept_name: continue

            if dept_name not in dept_stats:
                dept_stats[dept_name] = {'total_posts': 0, 'latest_snippets': [], 'logs': []}
            
            dept_stats[dept_name]['total_posts'] += 1
            dept_stats[dept_name]['logs'].append(log)

            is_duplicate = any(s['snippet'] == log['snippet'] for s in dept_stats[dept_name]['latest_snippets'])
            if not is_duplicate and len(dept_stats[dept_name]['latest_snippets']) < 2:
                dept_stats[dept_name]['latest_snippets'].insert(0, {'snippet': log['snippet'], 'sentiment': log['sentiment']})

    departments_data = []
    for config in DEPARTMENTS_CONFIG:
        name_lower = config['name'].lower()
        data = dept_stats.get(name_lower, {'total_posts': 0, 'latest_snippets': [], 'logs': []})
        departments_data.append({
            'name': config['name'].capitalize(),
            'img': config['img'], 
            'total_posts': data['total_posts'],
            'latest_snippets': data['latest_snippets'],
            'logs': data['logs']
        })

    return render_template('department.html', departments_data=departments_data)

@app.route('/statistics')
def statistics():
    sentiment_counts = {'Negative': 0, 'Neutral': 0, 'Positive': 0}
    for log in VERIFICATION_LOG:
        sentiment_counts[log['sentiment']] += 1

    bubble_data = []
    for log in VERIFICATION_LOG:
        bubble_data.append({
            'x': log['order'],
            'y': log['time_of_day'],
            'r': 10, 
            'sentiment': log['sentiment']
        })

    return render_template(
        'statistics.html', 
        sentiment_counts=sentiment_counts, 
        bubble_data=bubble_data,
        verification_log=VERIFICATION_LOG
    )

@app.route('/analyze_and_verify', methods=['POST'])
def analyze_and_verify():
    news_text = request.form.get('news_text', '')
    uploaded_file = request.files.get('news_image')
    
    final_text = news_text
    source = "Text Input"
    
    if uploaded_file and uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        
        ocr_text, source = perform_ocr(file_path)
        final_text = ocr_text if not news_text else news_text + " " + ocr_text
    
    if not final_text.strip():
        return render_template('index.html', verification_result="No news text or image provided.")

    # 1. Translation (on final_text)
    # The translated_text is used for analysis, but the original final_text is logged
    translated_text, detected_lang = translate_to_english(final_text) 

    # 2. Sentiment Analysis (on translated text)
    sentiment, polarity = analyze_sentiment(translated_text)
    
    # 3. Department Classification (on translated text)
    departments_str = classify_department(translated_text)

    # 4. Log the result (Original text, but results from translated text)
    log_verification(final_text, sentiment, polarity, departments_str, source, detected_lang)

    verification_result = f"{sentiment} news - {'Action required.' if sentiment != 'Neutral' else 'No action required.'}"
    
    return render_template(
        'index.html', 
        verification_result=verification_result,
        last_analysis={
            'text': final_text, 
            'sentiment': sentiment, 
            'departments': departments_str, 
            'source': source
        }
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)