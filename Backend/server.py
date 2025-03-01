import requests
from collections import defaultdict
from datetime import datetime
import pymongo
from flask import Flask, request, jsonify
from flask_cors import CORS
import finnhub
from datetime import datetime, timedelta
from models import analyze_sentiment_hugging_face,analyze_sentiment_text_blob
app = Flask(__name__)
CORS(app)

def create_connection():
    """Creates a connection to the MongoDB database."""
    client = pymongo.MongoClient("mongodb://docker:docker@localhost:27017/")
    return client["Pixel-pioneers-Indovate"]

db = create_connection()
news_collection = db["market_news"]
finnhub_client = finnhub.Client(api_key="cv19911r01qhkk81g1sgcv19911r01qhkk81g1t0")
DAILY_OPEN_CLOSE_URL="https://api.polygon.io/v1/open-close/AAPL/2025-02-20?adjusted=true&apiKey=IcrSwjkYMVxVvcHernNWoQRD0MSGwCXm"

#testing connection
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "MongoDB Flask API is running"}), 200


#search company sentiment using ticker
@app.route("/market-news/search", methods=["GET"])
def search_news_by_ticker():
    """Fetches news related to a specific stock ticker."""
    today = datetime.today().strftime('%Y-%m-%d')
    last_week = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d') 

    ticker = request.args.get("ticker", "").upper()
    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    stock_news = finnhub_client.company_news(symbol=ticker, _from=last_week, to=today)
    
    news_with_sentiment = []
    for article in stock_news:
        sentiment = analyze_sentiment_text_blob(article["headline"])
        article_entry = {
            "headline": article["headline"],
            "source": article["source"],
            "url": article["url"],
            "datetime": article["datetime"],
            "sentiment": sentiment,
            "ticker": ticker
        }
        news_with_sentiment.append(article_entry)

    return jsonify(news_with_sentiment)

#predict next day's opening and closing stock 
@app.route("/predict-stock")
def predict_ticker_stock():
    today = datetime.today().strftime('%Y-%m-%d')
    last_week = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d') 

    ticker = request.args.get("ticker", "").upper()
    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    response = requests.get(DAILY_OPEN_CLOSE_URL)
    return response.json()

    

if __name__ == "__main__":
    app.run(debug=True)

