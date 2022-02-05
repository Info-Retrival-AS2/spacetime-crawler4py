from bs4 import BeautifulSoup
import requests
url = "https://ics.uci.edu"
resp = requests.get(url)
from urllib.parse import urlparse

webResponse = BeautifulSoup(resp.content, parser='html.parser')
# print(webResponse.getText())
atag = webResponse.find_all('a')
for tag in atag:
    url = tag.get('href')
    parsed = urlparse(url)
    print(url)
# print(atag.get_text())
# parsed = urlparse(url)
# print(parsed.)

