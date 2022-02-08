import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import nltk
# nltk.download()
from nltk.corpus import stopwords
from simhash import Simhash, SimhashIndex

uniqueUrls = set()
tokens = dict()
maxTokenUrl = ""
maxTokenNum = 0
subdomains = dict() # <url, number of pages>



def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    # BeautifulSoup parse web
    response = BeautifulSoup(resp.raw_response.content, 'html.parser')

    # tokenize
    global maxTokenNum
    global maxTokenUrl
    nums = tokenize(response.get_text())
    if nums > maxTokenNum:
        maxTokenNum = nums
        maxTokenUrl = url

    # TODO: lyq
    # Find links
    uniquePages = [] # remove-dul is at isValid. Will be slow if use set here.
    # Find all href attr in a tags
    aTags = response.find_all('a')
    for tag in aTags:
        curUrl = tag.get('href')
        # eliminate the fragment
        isFragment = curUrl.find('#')
        if isFragment:
            curUrl = curUrl[:isFragment]
            uniquePages.append(curUrl)
        else:
            uniquePages.append(curUrl)







    #if *.ics.uci.edu, update global subdomains




    return uniquePages

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    # TODO: *.ics.uci.edu/* lyq
    # *.cs.uci.edu/*
    # *.informatics.uci.edu/*
    # *.stat.uci.edu/*
    domains = ['.ics.uci.edu', '.cs.uci.edu', '.informatics.uci.edu', '.stat.uci.edu', 'today.uci.edu/department/information_computer_sciences']
    try:
        parsed = urlparse(url)
        if parsed.hostname==None or parsed.netloc==None:
            return False
        if parsed.scheme not in set(["http", "https"]):
            return False
        # check like (ics.uci.edu) in (www.ics.uci.edu)
        if any(dom in parsed.hostname for dom in domains) and \
        not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            global uniqueUrls
            if url in uniqueUrls:
                return False
            else:
                uniqueUrls.add(url)
                return True


    except TypeError:
        print ("TypeError for ", parsed)
        raise
"""
responseText: web text string
return: number of tokens
ignore stopwrods
update maxTokenNum
"""
def tokenize(responseText):
    # TODO: jjy cy
    # nltk
    stopword = set(stopwords.words('english'))
    for w in ["aren't"]:  # TODO:其他停顿词
        stopword.add(w)
    responseTextLower = responseText.lower()
    tokenizer = RegexpTokenizer('[a-zA-Z0-9@#*&\']{2,}')
    wordTokens = tokenizer.tokenize(responseTextLower)
    removingStopwords = [word for word in wordTokens if word not in stopword]


    return len(removingStopwords)

    global tokens
    # update tokens


# TODO: output result

