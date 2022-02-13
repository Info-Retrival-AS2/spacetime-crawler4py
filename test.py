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
testUrl = "https://wics.ics.uci.edu/events/2019-11-01"
testUrl2 = "https://wics.ics.uci.edu/page/2"
parsed = urlparse(testUrl)
print(parsed.path.lower())
def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    domains = ['.ics.uci.edu', '.cs.uci.edu', '.informatics.uci.edu', '.stat.uci.edu',
               'today.uci.edu/department/information_computer_sciences']
    try:
        parsed = urlparse(url)
        if parsed.hostname == None or parsed.netloc == None:
            return False
        if parsed.scheme not in set(["http", "https"]) or (url.find("?") != -1) or (url.find("&") != -1):
            return False
        # check like (ics.uci.edu) in (www.ics.uci.edu)
        if any(dom in parsed.hostname for dom in domains) and \
                not re.match(
                    r"(.*\.(css|js|bmp|gif|jpe?g|ico"
                    + r"|png|tiff?|mid|mp2|mp3|mp4"
                    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                    + r"|ps|eps|tex|ppt|pptx|ppsx|pptm|xps|doc|docx|xls|xlsx|names"
                    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                    + r"|epub|dll|cnf|tgz|sha1"
                    + r"|thmx|mso|arff|rtf|jar|csv"
                    + r"|rm|smil|wmv|swf|wma|zip|rar|gz|z)$)"
                    , parsed.path.lower()) and \
                not re.search(
                    # r"pdf|docs|blog|events|date"
                    r"pdf|docs"
                    + r"|january|february|march|april|may|june|july|august|september|october|november|december"
                    + r"|jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec|"
                    + r"(19|20)[0-9]{2}-[0-9]{1,2}-[0-9]{1,2}", parsed.path.lower()):
                # not re.match(
                #     # r'/(19|20)[0-9]{2}/|/(19|20)[0-9]{2}$|/(19|20)[0-9]{2}-[0-9]{1,2}|/[0-9]{1,2}-(19|20)[0-9]{2}|[0-9]{1,2}-[0-9]{1,2}-(19|20)[0-9]{2}',
                #     # r'/(19|20)[0-9]{2}-[0-9]{1,2}|/[0-9]{1,2}-(19|20)[0-9]{2}|[0-9]{1,2}-[0-9]{1,2}-(19|20)[0-9]{2}|/(19|20)[0-9]{2}-[0-9]{1,2}-[0-9]{1,2}$',
                #     r".*(/(19|20)[0-9]{2}-[0-9]{1,2}-[0-9]{1,2})$",
                #     parsed.path.lower()):

            global uniqueUrls
            if url in uniqueUrls:
                return False
            else:
                uniqueUrls.add(url)
                return True
        else:
            return False

    except TypeError:
        print("TypeError for ", parsed)
        raise

print(is_valid(testUrl))

