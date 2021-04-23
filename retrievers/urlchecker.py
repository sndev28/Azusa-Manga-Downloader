from bs4 import BeautifulSoup

def urlchecker(url_object):

    ## ADD SUPPORT FOR NEW SITES HERE

    #Mangakakalot checks

    if url_object.find('ul', {'class':'row-content-chapter'}):
        return True

    elif url_object.find('div', {'class':'chapter-list'}):
        return True

    #End of all checks
    return False

