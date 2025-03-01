from transformers import pipeline
from textblob import TextBlob 


def analyze_sentiment_hugging_face(text):
    pipe = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",from_pt=True)

    # Set up a sentiment-analysis pipeline
    classifier = pipeline("sentiment-analysis")
    # Load model directly
    #from transformers import AutoTokenizer, AutoModelForSequenceClassification

    #tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
    #model = AutoModelForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
    result = classifier(text)
    return result


#sentiment analysis method
def analyze_sentiment_text_blob(text):
    """Analyze sentiment of a news headline using TextBlob."""
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity  # -1 (negative) to 1 (positive)
    if sentiment_score > 0:
        sentiment = "positive"
    elif sentiment_score < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return {"score": sentiment_score, "label": sentiment}

