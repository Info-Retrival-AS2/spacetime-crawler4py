from bs4 import BeautifulSoup
import requests
url = "https://www.ics.uci.edu"
resp = requests.get(url)

webResponse = BeautifulSoup(resp.content, parser='html.parser')
# print(webResponse.getText())
atag = webResponse.find('a')
print(atag.get_text())

