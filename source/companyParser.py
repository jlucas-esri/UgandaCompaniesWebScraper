from bs4 import BeautifulSoup
import pprint

class CompanyParser:

    def __init__(self, htmlText):
        self.htmlText = htmlText
        self.soup = BeautifulSoup(self.htmlText, features="html.parser")

    def convertInfoToDict(self):
        headerWithName = self.soup.find('ol', class_='breadcrumb hidden-sm-down')
        items = headerWithName.find_all(itemprop='itemListElement')
        companyNameItem = items[-1]
        companyName = companyNameItem.find(itemprop='name').get_text()
        # print(companyName)

        description = self.soup.find(itemprop='description').get_text()
        # print(description)
        address = self.soup.find(itemprop='address').find('meta')['content']
        # print(address)
        details = self.soup.find(class_='company-details-industry')
        labels = details.find_all('dt')
        values = details.find_all('dd')
        labelTextList = []
        valueTextList = []
        for label in labels:
            parsedText = label.get_text()
            parsedText = parsedText.replace(':', '')
            parsedText = parsedText.strip()
            labelTextList.append(parsedText)
        for value in values:
            parsedText = value.get_text()
            parsedText = parsedText.replace(':', '')
            parsedText = parsedText.strip()
            valueTextList.append(parsedText)

        correspondingLabelsWithValues = list(zip(labelTextList, valueTextList))
        detailsDict = {label: value for label, value in correspondingLabelsWithValues}

        panels = self.soup.find(id='productDescription').find_all(class_='panel')
        parsedPanels = self.parsePanels(panels)
        # print(detailsDict)
        # print(correspondingLabelsWithValues)
        # print(details)
        returnDict = {
            'name': companyName,
            'address': address,
            'details': detailsDict,
            'panels': parsedPanels
        }
        # pprint.pprint(returnDict)
        return returnDict
        # print(returnDict)

    def parsePanels(self, panels):
        panelDescList = []
        for panelItem in panels:
            panelTitle = panelItem.find('a').get_text().strip()
            panelDescDiv = panelItem.find(class_='panel-collapse collapse')
            panelDescPTags = panelDescDiv.find_all('p')
            fullDesc = '\n'.join([item.get_text().strip() for item in panelDescPTags])
            # print(panelTitle)
            panelDescDict = {
                'title': panelTitle,
                'description': fullDesc
            }
            # pprint.pprint(panelDescDict)
            panelDescList.append(panelDescDict)

        return panelDescList

    def main(self):
        return self.convertInfoToDict()
