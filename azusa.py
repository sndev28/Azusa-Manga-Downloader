

                                             ###############################################################################
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                 AZUSA                                       #
                                             #                                                                             #
                                             #                        VERSION CODE : 2.67.89                               #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             ###############################################################################





import requests
from bs4 import BeautifulSoup
from io import BytesIO
import os
import img2pdf
from PIL import Image
from zipfile import ZipFile
import shutil


cwd = os.getcwd()

def num_to_fourdigit(num):

    if len(str(num)) == 1:
        return f'000{num}'

    elif len(str(num)) == 2:
        return f'00{num}'

    elif len(str(num)) == 3:
        return f'0{num}'

    elif len(str(num)) == 4:
        return str(num)

def chapter_retrieve(chapter, format):


    try:
        url_object = BeautifulSoup(requests.get(chapter['Chapter URL']).text, 'lxml')

        panel_container = url_object.find('div', {'class' : 'container-chapter-reader'})

        panel_url = []

        panel_objects = panel_container.find_all('img')
        
        for obj in panel_objects:
            panel_url.append(obj['src'])

    except:
        os.system(f'del /q {cwd}\\temp\\*')
        return chapter


    img_objects = []
    file_names = [f'{cwd}\\splash.jpg']
    shutil.copy('0000.jpg', f'{cwd}\\temp')

    chapter_name = chapter["Chapter Name"]
    chapter_name = chapter_name.replace(':', '_')

    for index, url in enumerate(panel_url):

        file_name = num_to_fourdigit(index + 1)
        with open(f'{cwd}\\temp\\{file_name}.jpg', 'wb') as file:
            file.write(requests.get(url, headers = headers).content)
            file_names.append(f'{cwd}\\temp\\{file_name}.jpg')

    if format == 'pdf':

        pdf_name = f'{chapter_name}.pdf'
        
        with open(pdf_name, 'wb') as f:
            try : 
                f.write(img2pdf.convert(file_names))
            except img2pdf.AlphaChannelError:
                try:
                    for index, img in enumerate(file_names):
                        temp = Image.open(img)
                        temp = temp.convert('RGB')
                        img = img[:-4] + '_converted.jpg'
                        file_names[index] = img
                        temp.save(img)
                    f.write(img2pdf.convert(file_names))
                except:
                    os.system(f'del /q {cwd}\\temp\\*')
                    return chapter

            except:
                os.system(f'del /q {cwd}\\temp\\*')
                return chapter

    elif format == 'cbz':

        zip_name = f'{chapter_name}.zip'
        cbz_name = f'{chapter_name}.cbz'

        shutil.make_archive(chapter_name, 'zip', r'C:\Users\niyas\Desktop\Dev\Azusa\temp')
        
        os.rename(zip_name, cbz_name)

        os.system(f'del /q {cwd}\\temp\\*')

        return False


    os.system(f'del /q {cwd}\\temp\\*')

    return False


# initialization

os.system(f'del /q {cwd}\\temp\\*')

headers = {'referer':'https://manganelo.com/'}

chapter_url = 'https://manganelo.com/manga/kishuku_gakkou_no_juliet'

chapter_page = BeautifulSoup(requests.get(chapter_url).text, 'lxml')

chapter_frame = chapter_page.find('ul', {'class':'row-content-chapter'})

chapter_object = chapter_frame.find_all('li')

chapters = []

error_chapters = []

# chapters.append({
#         'Chapter Name' : chapter_object[2].a.text,
#         'Chapter URL' : chapter_object[2].a['href']
#     })

for chapter in chapter_object:
    chapters.append({
        'Chapter Name' : chapter.a.text,
        'Chapter URL' : chapter.a['href']
    })

while True:
    response = input('Which format do you want to download? (pdf/cbz)')
    if response == 'pdf' or response == 'cbz':
        break
    print('Wrong choice!!')


#start of image scraping

no_of_chapters = len(chapter_object)

for index, chapter in enumerate(chapters):

    print(index + 1 ,'/', no_of_chapters)

    iserror = chapter_retrieve(chapter, response)

    if iserror:
        error_chapters.append(iserror)


    

while(error_chapters != []):
    os.system('cls')
    print('\nChapters not downloaded : ')
    for chapter in error_chapters:
        print(chapter['Chapter Name'])

    response = input('Do you want me to attempt to downloaded the missing chapters? y/n')
    
    if response != 'y':
        break

    no_of_chapters = len(error_chapters)

    temp_error_chapters = []

    for index, chapter in enumerate(error_chapters):

        print(index + 1 ,'/', no_of_chapters)
        iserror = chapter_retrieve(chapter, response)

        if iserror:
            temp_error_chapters.append(iserror)

    error_chapters = temp_error_chapters

    temp_error_chapters = []



    


    






