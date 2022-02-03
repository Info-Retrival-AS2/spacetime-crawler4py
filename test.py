from bs4 import BeautifulSoup
import requests
url = "http://www.ics.uci.edu"
resp = requests.get(url)

webResponse = BeautifulSoup(resp.raw)

