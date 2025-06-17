#!/usr/bin/python3
import requests
import bs4
from extractor import extract


def extractNavSection(contentPage):
    """Extracts <a> tags from the navigation section of the Stardew Valley
    'All pages' wiki pages.
    
    Args:
        contentPage (str): URL of the content page to extract
    
    Returns: 
        List of <a> elements in the navigation section of the wiki page.
    """ 
    
    page = requests.get(contentPage, timeout=10)
        
    if not page.ok:
        page.raise_for_status()

    page.close()
    soup =  bs4.BeautifulSoup(page.text,'html.parser')
    
    navSection = soup.find('div',{'class':'mw-allpages-nav'})
    return navSection.find_all("a",recursive=False)

def doesNextPageExist(link:str):
    """ Checks if the stardew valley wiki page contains 
    the  link to the next page
    

    Args:
        link (str): URL of the content page to extract

    Returns:
       boolean: True if found, else returns False
    """    
    try: 
        
        linkElements = extractNavSection(link)
        
        for link in linkElements:
            if "Next page" in link.get_text():
                # return True
                print("Next Page exists:", link.get("href"))
                return True     
        print("Couldn't find next page")
        return False
        
    except Exception as err:
        print("Something went wrong when checking for next page:", err)
        return False

def getNextPageLink(link) :
    """Gets the "Next Page" link from the <a> tags returned by extractNavSection().

    Args:
        link (str): URL of the content page to extract the link

    Returns:
        str: Returns "Next page" link if found, else returns an empty string.
    """     
    linkElements = extractNavSection(link)
    for link in linkElements:
            if "Next page" in link.get_text():
                # return True
                return link.get("href")
    print("Couldn't get next page")
    return ''
    

def getLinks():
    """Function to return a list of all the pages containing links to extract
    info from.

    Returns:
       list: A list of links to the pages to extract is returned.
    """    
    baseUrl : str = 'https://stardewvalleywiki.com' 
    link: str = 'https://stardewvalleywiki.com/mediawiki/index.php?title=Special:AllPages&hideredirects=1'
    links = [link]
    
    while True:
        if doesNextPageExist(link):
            link = baseUrl + getNextPageLink(link)
            links.append( link )
        else:
            break
    
    return links

contentPages = getLinks()
extract(contentPages)