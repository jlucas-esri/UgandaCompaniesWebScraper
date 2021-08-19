import logging

from bs4.element import PageElement
from companyParser import CompanyParser
from htmlRetriever import HtmlRetriever
from companyIterator import CompanyIterator
from pageIterator import PageIterator
import json

logger = logging.getLogger('Scraper')
logging.basicConfig(level=logging.INFO)

def main():
    companyInformation = []
    initialLink = r'https://www.environmental-expert.com/waste-recycling/plastics-recycling/companies/location-africa'
    # initialLink = r'https://www.environmental-expert.com/waste-recycling/plastics-recycling/companies/location-uganda'
    pageGenerator = PageIterator(initialLink).main()
    for pageLink in pageGenerator:
        logger.info('Navigated to new page')
        # print(pageLink)
        mainPage = HtmlRetriever(pageLink).main()
        linkGenerator = CompanyIterator(mainPage).main()
        for link in linkGenerator:
            logger.info(f'Navigated to new link: "{link}"')
            # print(link) 
            companyContent = HtmlRetriever(link).main()
            returnDict = CompanyParser(companyContent).main()
            companyInformation.append(returnDict)
    
    logger.info(f'Number of companies retrieved: {len(companyInformation)}')
    fileName = 'companies.json'
    with open(fileName, 'w') as f:
        json.dump(companyInformation, f)

    logger.info(f'Companies written to file: "{fileName}"')
        
    # content = HtmlRetriever(r'https://www.environmental-expert.com/companies/digital-weighing-scales-shop-in-kampala-uganda-112092').main()
    # content = HtmlRetriever(r'https://www.environmental-expert.com/companies/aquila-recycling-industries-49873').main()
    # content = HtmlRetriever(r'https://www.environmental-expert.com/companies/eagle-weighing-systems-ltd-98121').main()
    # print(content)
    # returnDict = CompanyParser(content).main()

if __name__=='__main__':
    main()