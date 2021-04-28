import os
from bs4 import BeautifulSoup
import requests
import shutil
from urllib.parse import unquote
import string
import random
import concurrent.futures
from io import BytesIO
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

#helper functions

from retrievers.helpers import num_to_fourdigit



#Retriever

def chapter_retrieve(chapter, save_directory, chapter_no, serialize_flag):

    cwd = os.getcwd()


    #Making a new temporary directory

    #Retrieving!

    try:
        url_object = BeautifulSoup(requests.get(chapter['Chapter URL']).text, 'lxml')

        panel_container = url_object.find('div', {'class' : 'container-chapter-reader'})

        panel_objects = panel_container.find_all('img')
        
        panel_url = [unquote(obj['src']) for obj in panel_objects]

    except:
        return chapter


    #shutil.copy('0000.jpg', temp)

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

    
    headers = {'referer':'https://manganelo.com/'}


    session = requests.Session()


    cbz_name = f'{save_directory}\\{chapter_name}.cbz'


    archive = BytesIO()    

    with ZipFile(archive, 'w') as zip_archive:
        with open('0000.jpg', 'rb') as splash:
            img_file = ZipInfo('0000.jpg')
            img_file.compress_type = ZIP_DEFLATED
            zip_archive.writestr(img_file, splash.read())

        for index, url in enumerate(panel_url):
            file_name = num_to_fourdigit(index + 1)
            img_file = ZipInfo(file_name + '.jpg')
            img_file.compress_type = ZIP_DEFLATED
            data = session.get(url, headers = headers).content
            zip_archive.writestr(img_file, data)


    with open(cbz_name, 'wb') as file:
        file.write(archive.getbuffer())

    archive.close()

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