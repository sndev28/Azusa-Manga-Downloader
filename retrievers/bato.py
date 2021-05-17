import os
import requests
from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from io import BytesIO




#helper functions

from retrievers.helpers import num_to_fourdigit
from retrievers.py_exe import resource_path

#Retriever


def chapter_retrieve(chapter, save_directory, chapter_no, serialize_flag):

    cwd = os.getcwd()

    try:
        #initialzing headless chrome to get chapter list

        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options = Options()
        options.add_argument("--headless")
        options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(executable_path=resource_path('resources\\chromedriver.exe'), options = options)
        driver.get(chapter['Chapter URL'])

        url_objects = driver.find_elements_by_class_name('page-img')

        panel_url = [unquote(obj.get_attribute('src')) for obj in url_objects]


    except:
        return chapter

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

    if serialize_flag:
        chapter_name = str(chapter_no) + '_ ' + chapter_name


    session = requests.Session()


    cbz_name = f'{save_directory}\\{chapter_name}.cbz'

    archive = BytesIO()    

    with ZipFile(archive, 'w') as zip_archive:
        with open(resource_path('resources\\0000.jpg'), 'rb') as splash:
            img_file = ZipInfo('0000.jpg')
            img_file.compress_type = ZIP_DEFLATED
            zip_archive.writestr(img_file, splash.read())

        for index, url in enumerate(panel_url):
            file_name = num_to_fourdigit(index + 1)
            img_file = ZipInfo(file_name + '.jpg')
            img_file.compress_type = ZIP_DEFLATED
            data = session.get(url).content
            zip_archive.writestr(img_file, data)


    with open(cbz_name, 'wb') as file:
        file.write(archive.getbuffer())

    archive.close()

    return False




def chapter_meta_creator(site_url):

    #initialzing headless chrome to get chapter list

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(executable_path=resource_path('resources\\chromedriver.exe'), options = options)
    driver.get(site_url)
    
    chapter_objects = driver.find_elements_by_css_selector('.p-2.d-flex.flex-column.flex-md-row.item')

    chapters = [{'Chapter Name' : chapter.find_element_by_xpath('./a').text, 'Chapter URL' : chapter.find_element_by_xpath('./a').get_attribute('href')} for chapter in chapter_objects]

    driver.quit()    

    return chapters