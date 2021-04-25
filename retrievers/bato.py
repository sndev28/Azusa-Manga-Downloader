import os
from bs4 import BeautifulSoup
import requests
import shutil
from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options



#helper functions

from retrievers.helpers import num_to_fourdigit

#Retriever


def chapter_retrieve(chapter, save_directory):

    cwd = os.getcwd()

    #Making a new temporary directory

    temp = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
    os.mkdir(temp)

    try:
        #initialzing headless chrome to get chapter list

        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options = Options()
        options.add_argument("--headless")
        options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get(chapter['Chapter URL'])

        url_objects = driver.find_elements_by_class_name('page-img')

        panel_url = [unquote(obj.get_attribute('src')) for obj in url_objects]


    except:
        shutil.rmtree(temp)
        return chapter


    shutil.copy('0000.jpg', temp)

    chapter_name = chapter["Chapter Name"]

    #Editting file name to avoid file name error

    chapter_name = chapter_name.replace(':', '_')
    chapter_name = chapter_name.replace('<', '_')
    chapter_name = chapter_name.replace('>', '_')
    chapter_name = chapter_name.replace('\"', '_')
    chapter_name = chapter_name.replace('/', '_')
    chapter_name = chapter_name.replace('\\', '_')
    chapter_name = chapter_name.replace('|', '_')
    chapter_name = chapter_name.replace('?', '_')
    chapter_name = chapter_name.replace('*', '_')

    for index, url in enumerate(panel_url):

        file_name = num_to_fourdigit(index + 1)
        with open(f'{cwd}\\{temp}\\{file_name}.jpg', 'wb') as file:
            file.write(requests.get(url).content)



    zip_name = f'{save_directory}\\{chapter_name}.zip'
    cbz_name = f'{save_directory}\\{chapter_name}.cbz'

    shutil.make_archive(zip_name[:-4], 'zip', temp)
    
    try:
        os.rename(zip_name, cbz_name)
    except FileExistsError:
        os.remove(cbz_name)
        os.rename(zip_name, cbz_name)

    shutil.rmtree(temp)

    return False




def chapter_meta_creator(site_url):

    #initialzing headless chrome to get chapter list

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    driver.get(site_url)
    
    chapter_objects = driver.find_elements_by_css_selector('.p-2.d-flex.flex-column.flex-md-row.item')

    chapters = [{'Chapter Name' : chapter.find_element_by_xpath('./a').text, 'Chapter URL' : chapter.find_element_by_xpath('./a').get_attribute('href')} for chapter in chapter_objects]

    driver.quit()    

    return chapters