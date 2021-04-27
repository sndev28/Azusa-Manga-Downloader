import requests
from bs4 import BeautifulSoup

def urlchecker(link):

    ## ADD SUPPORT FOR NEW SITES HERE

    #Mangakakalot checks

    
    if 'manganelo' in link or 'mangakakalot' in link:
        url_object = BeautifulSoup(requests.get(link).text, 'lxml')
        if url_object.find('ul', {'class':'row-content-chapter'}):
            return True

        elif url_object.find('div', {'class':'chapter-list'}):
            return True


    #Bato.to check
    elif 'bato' in link:

        #initialzing headless chrome to get chapter list

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options = Options()
        options.add_argument("--headless")
        options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options = options)
        driver.get(link)

        try: 
            driver.find_element_by_css_selector('.p-2.d-flex.flex-column.flex-md-row.item')
            return True
        except:
            return False



    #End of all checks
    return False

