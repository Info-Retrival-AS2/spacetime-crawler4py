import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords

uniqueUrls = set()
tokens = dict()
maxTokenUrl = ""
maxTokenNum = 0
subdomains = dict()  # <url, number of pages>

outputCount = 500
stopword = []
for line in open("stopwords.txt"):
    word = line.strip("\n")
    stopword.append(word)


def scraper(url, resp):
    # there might be empty pages
    if resp.status != 200 or resp.raw_response.content == None:
        return []
    links = extract_next_links(url, resp)

    global outputCount
    if outputCount == 1:
        outputResult()
        outputCount = 500
    else:
        outputCount -= 1

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
    if nums <= 50:
        return []
    if nums > maxTokenNum:
        maxTokenNum = nums
        maxTokenUrl = url

    # TODO: lyq
    # Find links
    uniquePages = []  # remove-dul is at isValid. Will be slow if use set here.
    # Find all href attr in a tags
    aTags = response.find_all('a')
    for tag in aTags:
        curUrl = tag.get('href')
        if curUrl == None:
            continue
        # eliminate the fragment
        isFragment = curUrl.find('#')
        if isFragment != -1:
            curUrl = curUrl[:isFragment]
            uniquePages.append(curUrl)
        else:
            uniquePages.append(curUrl)

    return uniquePages


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
                    + r"|jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec|(19|20)[0-9]{2}-[0-9]{1,2}-[0-9]{1,2}", parsed.path.lower()):
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


"""
responseText: web text string
return: number of tokens
ignore stopwrods
update maxTokenNum
"""


def tokenize(responseText):
    # TODO: jjy cy
    # nltk
    # TODO: union or intersection?
    # stopword = set(stopwords.words('english'))
    global stopword

    responseTextLower = responseText.lower()
    tokenizer = RegexpTokenizer('[a-zA-Z0-9@#*&\']{2,}')
    wordTokens = tokenizer.tokenize(responseTextLower)
    removingStopwords = [word for word in wordTokens if word not in stopword]

    global tokens
    # update tokens
    if len(removingStopwords) <= 50:
        return len(removingStopwords)
    for token in removingStopwords:
        tokens[token] = tokens.get(token, 0) + 1
    return len(removingStopwords)


def get50Common():
    global tokens
    count = 50
    commonWords = []
    for word, freq in sorted(tokens.items(), reverse=True, key=lambda item: item[1]):
        if count == 0:
            break
        commonWords.append(word)
        count -= 1
    return commonWords


def getSubdomains(uniqueUrls):
    # update from the nearest uniqueUrls, so clear at each time
    global subdomains
    subdomains.clear()
    for url in uniqueUrls:
        parsed = urlparse(url)
        if 'ics.uci.edu' in parsed.netloc.lower():
            subdomains[parsed.hostname] = subdomains.get(parsed.hostname, 0) + 1


def outputResult():
    global uniqueUrls, maxTokenUrl, maxTokenNum
    output = "1. Number of unique pages found: " + str(len(uniqueUrls)) + "\n\n" \
             + "2. Longest page in terms of number of tokens:\n " + maxTokenUrl + " " + str(maxTokenNum) + "\n\n" \
             + "3. 50 most common words: \n"
    commonWords = get50Common()
    for word in commonWords:
        output += word + "\n"
    output += "\n4. Subdomains:\n"
    getSubdomains(uniqueUrls)
    global subdomains
    for sub, num in sorted(subdomains.items()):
        output += sub + ",  " + str(num) + "\n"
    try:
        f = open("result.txt", "x")
    except:
        f = open("result.txt", "w")
    finally:
        f.write(output)
        f.close()
