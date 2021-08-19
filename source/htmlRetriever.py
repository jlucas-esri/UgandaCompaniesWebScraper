import requests

class HtmlRetriever:

    def __init__(self, link):
        self.link = link

        self.content = requests.get(link).content

    def main(self):
        return self.content
        
        