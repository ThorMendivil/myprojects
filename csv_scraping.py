import requests
from bs4 import BeautifulSoup
from csv import DictWriter
from time import sleep

BASE_URL = "http://quotes.toscrape.com/"


def scrape_quotes():
    url = "/page/1"
    all_quotes = []
    while url:
        res = requests.get(f"{BASE_URL}{url}")
        print(f"Now Scrapping {BASE_URL}{url}...")
        # Procedure for new page
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            all_quotes.append({
                'text': quote.find(class_="text").get_text(),
                'author': quote.find(class_="author").get_text(),
                'bio-link': quote.find("a")["href"]
            })
        # button for next page
        nxt_btn = soup.find(class_="next")
        url = nxt_btn.find("a")["href"] if nxt_btn else None
        sleep(1)  # STANDARD PROTOCOL
    return all_quotes


def write_quotes(quotes):
    # write quotes to csv file
    with open("quotes.csv", "w") as f:
        headers = ['text', 'author', 'bio-link']
        csv_writer = DictWriter(f, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)


quotes = scrape_quotes()
write_quotes(quotes)
