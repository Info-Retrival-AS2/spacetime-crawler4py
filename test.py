from bs4 import BeautifulSoup
import requests
url = "https://ics.uci.edu"
resp = requests.get(url)
from urllib.parse import urlparse
import nltk
from nltk.corpus import stopwords
htmlfile = open('test.html', 'r', encoding='utf-8')
htmlhandle = htmlfile.read()
webResponse = BeautifulSoup(htmlhandle, parser='html.parser')
text = webResponse.getText()
f = open('output.txt', 'w', encoding='utf-8')
f.write(text)
# print(text)
# atag = webResponse.find_all('a')
# for tag in atag:
#     url = tag.get('href')
#     parsed = urlparse(url)
#     print(url)
# stops = stopwords.words('english')
# print(stops)

