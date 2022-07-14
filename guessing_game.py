import requests
from bs4 import BeautifulSoup
from csv import DictReader
from random import choice

BASE_URL = "http://quotes.toscrape.com/"

def read_quotes(filename):
    with open(filename, "r") as f:
        cvs_reader = DictReader(f)
        return list(cvs_reader)


def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    print("Here's a quote: ")
    print(quote['text'])
    print(quote['author'])
    guess = ''
    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses} ")
        remaining_guesses -= 1
        if guess.lower() == quote["author"].lower():
            print("YOU WIN")

        elif remaining_guesses == 3:
            # Click the ABOUT button
            res = requests.get(f"{BASE_URL}{quote['bio-link']}")
            # Procedure for new page
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(f"Here's a hint: The author was born in {birth_place} on {birth_date}")

        elif remaining_guesses == 2:
            first_initial = quote['author'][0]
            print(f"Here's a hint: The author first initial is {first_initial}")

        elif remaining_guesses == 1:
            last_initial = quote['author'].split(" ")[1][0]
            print(f"Here's a hint: The author last initial is {last_initial}")

        else:
            print(f"Sorry you ran out of guesses. The answer is {quote['author']}")

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (y/n)?")
    if again.lower() in ('yes', 'y'):
        print("Okay lets play again!")
        return start_game(quotes)
    else:
        print("Okay, GOODBYE!")


quotes = read_quotes("quotes.csv")
start_game(quotes)
