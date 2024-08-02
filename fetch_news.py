import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load the variables from .en file
load_dotenv()

# Get the API keys
news_api_key = os.getenv('news_api_key')

# Make sure the API key has loaded correctly
if not api_key:
    raise ValueError("API key not found. Please, add it to the .env file")

# Define the endpoint and parameters
url = 'https://newsapi.org/v2/everything'


# Calculate the date for the 'from' parameter (yesterday's date)
yesterday = datetime.now() - timedelta(1)
from_date = yesterday.strftime('%Y-%m-%d')
today = datetime.now()

# Define the API parameters
params = {
    'q': 'Trump OR Biden OR Harris',
    'from': from_date,
    'sortBy': 'popularity',
    'apiKey': news_api_key
}

# Make the GET request with the parameters
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # List to store article data
    articles_list = []
    
    # Iterate over the articles and extract relevant information
    for article in data['articles']:
        articles_list.append({
            'Title': article['title'],
            'Author': article.get('author', 'No author'),
            'Source': article['source']['name'],
            'Published At': article['publishedAt'],
            'Description': article['description'],
            'Content': article['content'],
            'URL': article['url']
        })
    
    # Create a DataFrame
    new_articles_df = pd.DataFrame(articles_list)
    
    ########## I should do the data transformation here ###########
    # Append the new articles to the existing CSV file
    file_path = 'news_articles.csv'
    try:
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, new_articles_df], ignore_index=True)
        updated_df.to_csv(file_path, index=False)
    except FileNotFoundError:
        new_articles_df.to_csv(file_path, index=False)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
