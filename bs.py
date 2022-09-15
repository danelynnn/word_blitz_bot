import requests
from bs4 import BeautifulSoup

url = "https://www.wordcheats.com/wordlist/words-with-friends/2-letter-words"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
tag = soup.find('ul', {'id': 'word-list'})

children = tag.findChildren("li" , recursive=False)
words = '\n'.join([child.contents[0] for child in children])
file = open('scrape.out', 'w+')
file.write(words)
