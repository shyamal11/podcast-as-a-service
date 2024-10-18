import requests
from bs4 import BeautifulSoup
import datetime
import re
import os
from dotenv import load_dotenv
from openai import OpenAI
from django.conf import settings
import json



def load_api_client():
    client = OpenAI(api_key= os.environ.get("OPENAI_API_KEY"))
    return client

def is_today(date_input, current_date):
    if isinstance(date_input, datetime.datetime):
        return date_input.date() == current_date
    elif isinstance(date_input, str):
        match = re.search(r'(\d{4}/\d{1,2}/\d{1,2})', date_input)
        if match:
            date_part = match.group(1)
            parsed_date = datetime.datetime.strptime(date_part, "%Y/%m/%d").date()
            return parsed_date == current_date
    return False

def scrape_verge(current_date):
    url = 'https://www.theverge.com/tech'
    base_url = 'https://www.theverge.com'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('a', {'class': 'group hover:text-white'})
    articles = [[item.get('aria-label'), base_url + item['href']] for item in items if is_today(item['href'], current_date)]
    return articles

def scrape_cnbctech(current_date):
    url = 'https://www.cnbc.com/technology/'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article_cards = soup.find_all('div', class_='Card-standardBreakerCard')
    articles = []

    for card in article_cards:
        title_tag = card.find('a', class_='Card-title')
        time_tag = card.find('span', class_='Card-time')
        if title_tag and time_tag:
            title = title_tag.text.strip()
            link = title_tag['href']
            publication_time = time_tag.text.strip()
            date_object = parse_publication_date(publication_time)
            if is_today(date_object, current_date):
                articles.append([title, link])
    return articles

def parse_publication_date(publication_time):
    date_str = re.sub(r'(st|nd|rd|th)', '', publication_time)
    try:
        return datetime.datetime.strptime(date_str, '%a, %b %d %Y')
    except ValueError:
        return datetime.datetime.today()

def scrape_techcrunch(current_date):
    url = 'https://techcrunch.com/'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    data_links = soup.find_all('a', attrs={'data-destinationlink': True})
    
    articles = [[link.text.strip(), link['href']] for link in data_links if is_today(link['href'], current_date) and link.text.strip()]
    return articles


def scrape_and_group_by_source(current_date):
    sources = {
        'TechCrunch': scrape_techcrunch(current_date),
        'The Verge': scrape_verge(current_date),
        'CNBC Tech': scrape_cnbctech(current_date),
    }

    return sources


def format_grouped_titles_by_source(grouped_sources):
    formatted_text = ""
    for source, articles in grouped_sources.items():
        formatted_text += f"{source}\n" + \
            "\n".join(title for title, _ in articles) + "\n\n"
    return formatted_text.strip()

def scrape_all_news(current_date):
    news_list = scrape_verge(current_date) + scrape_cnbctech(current_date) + scrape_techcrunch(current_date)
    print(str(len(news_list)) + " news articles scraped.")
    titles = [x[0] for x in news_list]
    news_to_URL = {news[0].lower(): news[1] for news in news_list}


    return  news_to_URL





