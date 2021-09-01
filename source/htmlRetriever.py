import requests

class HtmlRetriever:

    def __init__(self, link):
        self.link = link
        self.response = requests.get(link)
        self.response.raise_for_status()
        self.content = self.response.content

    def main(self):
        return self.content
        
        