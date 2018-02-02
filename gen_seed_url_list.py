from bs4 import BeautifulSoup
import requests

# url = 'https://en.wikipedia.org/wiki/Computer_science'
urls = ['https://en.wikipedia.org/wiki/Life','https://en.wikipedia.org/wiki/Human','https://en.wikipedia.org/wiki/History_of_the_world','https://en.wikipedia.org/wiki/Culture','https://en.wikipedia.org/wiki/Language','https://en.wikipedia.org/wiki/The_arts','https://en.wikipedia.org/wiki/Science','https://en.wikipedia.org/wiki/Technology','https://en.wikipedia.org/wiki/Mathematics']

if __name__ == '__main__':
    for url in urls:
        content = requests.get(url).content
        soup = BeautifulSoup(content, "lxml")
        res = set()
        for l in list(soup.findAll("a")):
            s = l.get('href')
            if type(s) == str and 'http://en.wikipedia' in s:
                res.add(s)
            if type(s) == str and s[:6] == '/wiki/':
                res.add('https://en.wikipedia.org' + s)
        for s in res:
            print(s)
