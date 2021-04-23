import os
from bs4 import BeautifulSoup
import requests
import shutil
from urllib.parse import unquote

#helper functions

from retrievers.helpers import num_to_fourdigit

#Retriever

def chapter_retrieve(chapter, save_directory):

    cwd = os.getcwd()

    #print('Retrieving!')

    headers = {'referer':'https://manganelo.com/'}

    try:
        url_object = BeautifulSoup(requests.get(chapter['Chapter URL']).text, 'lxml')

        panel_container = url_object.find('div', {'class' : 'container-chapter-reader'})

        panel_url = []

        panel_objects = panel_container.find_all('img')
        
        for obj in panel_objects:
            panel_url.append(unquote(obj['src']))

    except:
        os.system(f'del /q {cwd}\\temp\\*')
        return chapter


    img_objects = []
    file_names = [f'{cwd}\\0000.jpg']
    shutil.copy('0000.jpg', f'{cwd}\\temp')

    chapter_name = chapter["Chapter Name"]
    chapter_name = chapter_name.replace(':', '_')

    for index, url in enumerate(panel_url):

        file_name = num_to_fourdigit(index + 1)
        with open(f'{cwd}\\temp\\{file_name}.jpg', 'wb') as file:
            file.write(requests.get(url, headers = headers).content)
            file_names.append(f'{cwd}\\temp\\{file_name}.jpg')



    zip_name = f'{save_directory}\\{chapter_name}.zip'
    cbz_name = f'{save_directory}\\{chapter_name}.cbz'

    shutil.make_archive(zip_name[:-4], 'zip', f'{cwd}\\temp')
    
    try:
        os.rename(zip_name, cbz_name)
    except FileExistsError:
        os.remove(cbz_name)
        os.rename(zip_name, cbz_name)

    os.system(f'del /q {cwd}\\temp\\*')

    return False




def chapter_meta_creator(site_url):

    chapter_page = BeautifulSoup(requests.get(site_url).text, 'lxml')
    
    chapters = []

    if chapter_page.find('ul', {'class':'row-content-chapter'}):

        chapter_frame = chapter_page.find('ul', {'class':'row-content-chapter'})

        chapter_object = chapter_frame.find_all('li')

        for chapter in chapter_object:
            chapters.append({
                'Chapter Name' : chapter.a.text,
                'Chapter URL' : chapter.a['href']
            })

    elif chapter_page.find('div', {'class':'chapter-list'}):
        chapter_frame = chapter_page.find('div', {'class':'chapter-list'})

        chapter_object = chapter_frame.find_all('a')

        for chapter in chapter_object:  
            chapters.append({
                'Chapter Name' : chapter.text,
                'Chapter URL' : chapter['href']
            })

    return chapters