from bs4 import BeautifulSoup
import requests
url = "https://ics.uci.edu"
resp = requests.get(url)
import  re
from urllib.parse import urlparse
import nltk
from nltk.corpus import stopwords
# htmlfile = open('test.html', 'r', encoding='utf-8')
# htmlhandle = htmlfile.read()
# webResponse = BeautifulSoup(htmlhandle, parser='html.parser')
# text = webResponse.getText()
# f = open('output.txt', 'w', encoding='utf-8')
# f.write(text)
# print(text)
# atag = webResponse.find_all('a')
# for tag in atag:
#     url = tag.get('href')
#     parsed = urlparse(url)
#     print(url)
# stops = stopwords.words('english')
# print(stops)
testUrl = "https://www.informatics.uci.edu/2014/07"
testUrl2 = "https://wics.ics.uci.edu/page/2"
parsed = urlparse(testUrl)
print(parsed.path.lower())
if re.match(
                    r'/(19|20)[0-9]{2}/',
                    "/2020/10/01"):
    print(1)

