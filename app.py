from flask import Flask, render_template, jsonify
from textblob import TextBlob
import requests

app = Flask(__name__)

# Your News API key
API_KEY = '6693e0ad97384e768f3f8396a69fdd95'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'

def fetch_news(api_key):
    params = {
        'country': 'in',
        'apiKey': api_key,
    }
    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def news_api():
    news_data = fetch_news(API_KEY)
    articles = news_data.get('articles', [])
    sentiments = [{'title': article['title'], 'sentiment': analyze_sentiment(article['title']), 'url': article['url']} for article in articles]
    return jsonify(sentiments)

if __name__ == "__main__":
    app.run(debug=True)
