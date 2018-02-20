import logging
from datamodel.search.Charlit1GiremadzAguarda2_datamodel import Charlit1GiremadzAguarda2Link, OneCharlit1GiremadzAguarda2UnProcessedLink, add_server_copy, get_downloaded_content
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, ServerTriggers
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4

from urlparse import urlparse, parse_qs
from uuid import uuid4

logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"

@Producer(Charlit1GiremadzAguarda2Link)
@GetterSetter(OneCharlit1GiremadzAguarda2UnProcessedLink)
@ServerTriggers(add_server_copy, get_downloaded_content)
class CrawlerFrame(IApplication):

    def __init__(self, frame):
        self.starttime = time()
        self.app_id = "Charlit1GiremadzAguarda2"
        self.frame = frame


    def initialize(self):
        self.count = 0
        l = Charlit1GiremadzAguarda2Link("http://www.ics.uci.edu/")
        print l.full_url
        self.frame.add(l)

    def update(self):
        unprocessed_links = self.frame.get(OneCharlit1GiremadzAguarda2UnProcessedLink)
        if unprocessed_links:
            link = unprocessed_links[0]
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            links = extract_next_links(downloaded)
            for l in links:
                if is_valid(l):
                    self.frame.add(Charlit1GiremadzAguarda2Link(l))
                    # Dictionary { subdomain: num of URLs processed }
                    # Dictionary { links: number of out links from it }
                    # Dictionary { links: number of in links to it }

    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")


def extract_next_links(rawDataObj):
    outputLinks = []

    '''
    rawDataObj is an object of type UrlResponse declared at L20-30
    datamodel/search/server_datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded. 
    The frontier takes care of that.
    
    Suggested library: lxml
    '''
    links = re.findall(r'(?<=<a href=")[^"]*', rawDataObj.content)
    if rawDataObj.url[-1] != '/': # normalize input URL with '/'
        rawDataObj.url += '/'

    for val in links:
        if val[-1] != '/':  # normalize link with '/'
            val += '/'

        if val.startswith("https://") or val.startswith("http://"):
            outputLinks += val
        outputLinks += urlparse.urljoin(rawDataObj.url, val)
    print(outputLinks)

    return outputLinks

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.
    '''
    parsed = urlparse(url)
    if parsed.scheme not in set(["http", "https"]):
        return False
    try:
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz|javascript:|mailto:|@|#)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False