import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "http://quotes.toscrape.com"

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def scrape_quotes_and_authors():
    quotes = []
    authors = []
    authors_info = {}

    url = BASE_URL
    while url:
        soup = get_soup(url)
        quote_divs = soup.find_all("div", class_="quote")
        
        for quote_div in quote_divs:
            text = quote_div.find("span", class_="text").get_text()
            author = quote_div.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote_div.find_all("a", class_="tag")]
            
            quotes.append({
                "quote": text,
                "author": author,
                "tags": tags
            })
            
            if author not in authors_info:
                author_url = BASE_URL + quote_div.find("a")["href"]
                author_soup = get_soup(author_url)
                born_date = author_soup.find("span", class_="author-born-date").get_text()
                born_location = author_soup.find("span", class_="author-born-location").get_text()
                description = author_soup.find("div", class_="author-description").get_text().strip()
                
                authors_info[author] = {
                    "name": author,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                }
        
        next_page = soup.find("li", class_="next")
        url = BASE_URL + next_page.find("a")["href"] if next_page else None
        time.sleep(1)  # Polite delay

    authors = list(authors_info.values())

    return quotes, authors

quotes, authors = scrape_quotes_and_authors()

# Save to quotes.json
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes, f, ensure_ascii=False, indent=4)

# Save to authors.json
with open("authors.json", "w", encoding="utf-8") as f:
    json.dump(authors, f, ensure_ascii=False, indent=4)
