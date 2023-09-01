from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()
api_token2 = os.getenv("MARKETAUX_TOKEN")

def get_news(ticker,daysprior=14):
    base_url = "https://api.marketaux.com/v1/news/all"
    api_token = api_token2

    # Calculate the date 14 days ago from today's date
    publish_after_date = (datetime.now() - timedelta(days=daysprior)).strftime('%Y-%m-%dT%H:%M:%S')
    symbol = str(ticker)
    limit = 3
    query_params = {
        "exchanges": "NYSE,NASDAQ",
        "symbols": symbol,
        "countries": "us",
        "language": "en",
        "group_similar": "true",
        "limit": limit,
        "published_after": publish_after_date,
        "api_token": api_token
    }

    response = requests.get(base_url, params=query_params)

    if response.status_code == 200:
        news_data = response.json()
        # Process the 'news_data' as needed
        
        if "{'meta': {'found': 0, 'returned': 0, " in str(news_data):
            return("No news found on " + str(symbol) + " as of " + str(publish_after_date))

        data = ""
        for i in range(int(news_data['meta']['returned'])):
            data = data + "- **" + str(news_data['data'][i]['published_at'])[:str(news_data['data'][i]['published_at']).index(".")] + "** " + str(news_data['data'][i]['title']) + " [link](" + str(news_data['data'][i]['url']) + ")\n"

        return(data)
    else:
        print(f"Request failed with status code: {response.status_code}")
        return(response.text)