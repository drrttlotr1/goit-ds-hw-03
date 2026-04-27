import requests
from bs4 import BeautifulSoup
import json

def get_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = []
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author_tag = quote.find('small', class_='author')
        author = author_tag.text if author_tag else "Unknown"
        author_page_url_tag = quote.find('a', href=True)
        author_page_url = author_page_url_tag['href'] if author_page_url_tag else None

        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        quotes.append({
            'quote': text,
            'author': author,
            'author_page_url': author_page_url,
            'tags': tags
        })
    return quotes

def get_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    fullname = soup.find('h3', class_='author-title').text.strip() if soup.find('h3', class_='author-title') else "N/A"
    born_date = soup.find('span', class_='author-born-date').text.strip() if soup.find('span', class_='author-born-date') else "N/A"
    born_location = soup.find('span', class_='author-born-location').text.strip() if soup.find('span', class_='author-born-location') else "N/A"
    description = soup.find('div', class_='author-description').text.strip() if soup.find('div', class_='author-description') else "N/A"
    
    return {
        'fullname': fullname,
        'born_date': born_date,
        'born_location': born_location,
        'description': description
    }

def scrapy_all_quotes():
    base_url = 'http://quotes.toscrape.com'
    page_url = base_url
    all_quotes = []
    authors_info = {}
    
    while page_url:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'lxml')
        
        quotes = get_quotes(page_url)
        all_quotes.extend(quotes)

        for quote in quotes:
            author = quote['author']
            author_page_url = quote['author_page_url']
            if author_page_url and author not in authors_info:
                authors_info[author] = get_author_details(base_url + author_page_url)

        next_page = soup.find('li', class_='next')
        if next_page:
            page_url = base_url + next_page.find('a')['href']
        else:
            page_url = None

    return all_quotes, authors_info

quotes, authors = scrapy_all_quotes()

with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes, f, indent=4, ensure_ascii=False)

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(list(authors.values()), f, indent=4, ensure_ascii=False)
    
print("Скрапінг завершено!")