import requests
import bs4

def contains_slash(title):
    return "/" in title  # Returns True if '/' is found, False otherwise


def sanitizeTitle(titleValue) : 
    if titleValue.startswith("'") and titleValue.endswith("'"):
        titleValue = titleValue[1:-1]

    if contains_slash(titleValue):
        titleValue = titleValue.replace("/", "-")

    return titleValue


def getLinkTags(link):
    page = requests.get(link, timeout=10)
        
    if not page.ok:
        page.raise_for_status()

    page.close()
    
    soup =  bs4.BeautifulSoup(page.text,'html.parser')
    
    return soup.select(" .mw-allpages-chunk li a")
    

def extract(links):
    """Extracts all the info in raw format from the wiki pages and saves them in info/ dir

    Args:
        links (list): List of all the pages containing links to the articles to be stored.
    """
    articles = []
    
    for link in links:
    
        articleLinks = getLinkTags(link)

        for articleLink in articleLinks:
            hrefValue = articleLink.get('href')
            titleValue = articleLink.getText()
            
            titleValue = sanitizeTitle(titleValue)
            
            
            articles.append(
                {
                    'link' : 'https://stardewvalleywiki.com' + hrefValue + '?action=raw',
                    'title': titleValue
                })
    
    for article in articles:
        
        print(f"Downloading {article['title']} at {article['link']} \n")    
        response = requests.get(article['link'],timeout=10)
        text = response.text
        
        response.close()
        
        fileName = f"info/{article['title']}.txt"
        with open(fileName, "w") as file:
            file.write(text)
            file.close()
    
