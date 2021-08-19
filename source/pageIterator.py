from bs4 import BeautifulSoup
import logging
import time
from htmlRetriever import HtmlRetriever

class PageIterator:

    def __init__(self, link):
        self.link = link



    def iteratePages(self):
        morePages = True
        #yield the first link before anything
        yield self.link
        link = self.link

        while morePages:

            #setup
            self.content = HtmlRetriever(link).main()
            self.soup = BeautifulSoup(self.content, features='html.parser')

            self.paginator = self.soup.find('nav', class_='pagination')
            if self.paginator is None:
                break
            self.linkATags = self.paginator.find_all(class_='page-link')

            nextLink = self.linkATags[-1]['href']

            if nextLink == '#':
                break
            else:
                # time.sleep(1)
                link = nextLink
                yield nextLink

    def main(self):
        return self.iteratePages()

