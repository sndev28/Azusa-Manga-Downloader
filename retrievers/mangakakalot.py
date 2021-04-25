import os
from bs4 import BeautifulSoup
import requests
import shutil
from urllib.parse import unquote
import string
import random
import concurrent.futures

#helper functions

from retrievers.helpers import num_to_fourdigit



#Retriever

def chapter_retrieve(chapter, save_directory):

    cwd = os.getcwd()


    #Making a new temporary directory

    temp = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
    os.mkdir(temp)

    #Retrieving!

    try:
        url_object = BeautifulSoup(requests.get(chapter['Chapter URL']).text, 'lxml')

        panel_container = url_object.find('div', {'class' : 'container-chapter-reader'})

        panel_objects = panel_container.find_all('img')
        
        panel_url = [unquote(obj['src']) for obj in panel_objects]

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

    
    headers = {'referer':'https://manganelo.com/'}


    session = requests.Session()
                

    for index, url in enumerate(panel_url):

        file_name = num_to_fourdigit(index + 1)

        with open(f'{cwd}\\{temp}\\{file_name}.jpg', 'wb') as file:
            file.write(session.get(url, headers = headers).content)



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

    chapter_page = BeautifulSoup(requests.get(site_url).text, 'lxml')

    if chapter_page.find('ul', {'class':'row-content-chapter'}):

        chapter_frame = chapter_page.find('ul', {'class':'row-content-chapter'})

        chapter_objects = chapter_frame.find_all('li')

        chapters = [{'Chapter Name' : chapter.a.text,'Chapter URL' : chapter.a['href']} for chapter in chapter_objects]

    elif chapter_page.find('div', {'class':'chapter-list'}):
        chapter_frame = chapter_page.find('div', {'class':'chapter-list'})

        chapter_objects = chapter_frame.find_all('a')

        chapters = [{'Chapter Name' : chapter.text,'Chapter URL' : chapter['href']} for chapter in chapter_objects]

    return chapters