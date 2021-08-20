from bs4 import BeautifulSoup
import pprint
import re

class CompanyParser:

    def __init__(self, htmlText, link):
        self.htmlText = htmlText
        self.link = link
        self.id = re.split(r'\-', self.link)[-1]
        self.soup = BeautifulSoup(self.htmlText, features="html.parser")

    def _returnSafeAddressVal(self, tag, itemprop, default=''):
        if tag is not None:
            if tag.find('meta', itemprop=itemprop) is not None:
                text = tag.find('meta', itemprop=itemprop)['content']
                if text is None:
                    return default
                return text
            
            elif tag.find('span', itemprop=itemprop) is not None:
                text = tag.find('span', itemprop=itemprop).get_text()
                if text is None:
                    return default 
                return text

            else:
                return default
        else:
            return default


    def convertInfoToDict(self):
        headerWithName = self.soup.find('ol', class_='breadcrumb hidden-sm-down')
        items = headerWithName.find_all(itemprop='itemListElement')
        companyNameItem = items[-1]
        companyName = companyNameItem.find(itemprop='name').get_text()
        # print(companyName)

        descriptionItem = self.soup.find(itemprop='description')
        if descriptionItem is not None:
            description = descriptionItem.get_text()
        else:
            description = None

        addressItem = self.soup.find(itemprop='address')
        streetAddress = self._returnSafeAddressVal(addressItem, 'streetAddress')
        addressLocality = self._returnSafeAddressVal(addressItem, 'addressLocality')
        addressRegion = self._returnSafeAddressVal(addressItem, 'addressRegion') 
        postalCode = self._returnSafeAddressVal(addressItem, 'postalCode')
        addressCountry = self._returnSafeAddressVal(addressItem, 'addressCountry')
        # print(repr(addressComponentList))

        if not '' in [streetAddress, addressLocality] or not '' in [streetAddress, addressRegion]:
            streetAddress = streetAddress + ','
        if not '' in [addressLocality, addressRegion]:
            addressLocality = addressLocality + ','

        addressComponentList = [streetAddress, addressLocality, addressRegion, postalCode, addressCountry]
        addressText = ' '.join(addressComponentList)


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

        panelContainer = self.soup.find(id='productDescription')

        if panelContainer is not None:
            panels = panelContainer.find_all(class_='panel')
            parsedPanels = self.parsePanels(panels)
        else:
            parsedPanels = []
        # print(detailsDict)
        # print(correspondingLabelsWithValues)
        # print(details)
        returnDict = {
            'link': self.link,
            'id': self.id,
            'name': companyName,
            'description': description,
            'address': addressText,
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
