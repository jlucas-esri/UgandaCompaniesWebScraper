from bs4 import BeautifulSoup

class CompanyIterator:

    def __init__(self, content):
        self.content = content
        self.soup = BeautifulSoup(self.content, features='html.parser')

    def getCompanyLinks(self):
        productList = self.soup.find(class_='product-list')
        companyItems = productList.find_all(class_='product-item')
        for item in companyItems:
            companyATag = item.find('h2').find('a')
            link = companyATag['href']
            # print(link)
            yield link

    def main(self):
        return self.getCompanyLinks()
