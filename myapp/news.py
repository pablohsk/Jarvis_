import requests
from bs4 import BeautifulSoup

class News:
    def __init__(self):
        self.url = "https://www.reuters.com/"
        self.articles = []

    def fetch_headlines(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        headlines = soup.find_all("h3", class_="article-heading")
        for headline in headlines:
            self.articles.append(headline.text)

    def speak_headlines(self):
        self.fetch_headlines()
        if len(self.articles) == 0:
            print("Sorry, I couldn't find any news.")
        else:
            print("Here are the latest headlines:")
            for i, article in enumerate(self.articles):
                print(f"Headline {i+1}: {article}")
