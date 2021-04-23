

                                             ###############################################################################
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                 AZUSA                                       #
                                             #                                                                             #
                                             #                        VERSION CODE : 2.69.87                               #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             ###############################################################################





from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

import requests
from bs4 import BeautifulSoup
from io import BytesIO
import os
import img2pdf
from PIL import Image
import shutil
from threading import Thread
from urllib.parse import unquote


Window.size = (900,660)


Builder.load_file('azusa.kv')

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

def chapter_retrieve(chapter, format, save_directory):

    print('Retrieving!')

    #mangakakalot

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


    os.system(f'del /q {cwd}\\temp\\*')

    return False


def downloader(kivy_object):

    kivy_object.ids.download_status.text = 'Downloading under progress!'
    kivy_object.ids.batch_download.disable = True
    kivy_object.ids.directory.readonly = True
    kivy_object.ids.url.readonly = True

    if not os.path.exists(f'{cwd}\\temp'):
        os.mkdir(f'{cwd}\\temp')
    os.system(f'del /q {cwd}\\temp\\*')

    chapters = []

    error_chapters = []

    chapter_url = kivy_object.ids.url.text

    chapter_page = BeautifulSoup(requests.get(chapter_url).text, 'lxml')

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

    else:
        kivy_object.ids.url.text = 'Wrong url!'
        return

            

    no_of_chapters = len(chapter_object)
    kivy_object.ids.download_progress.max = no_of_chapters

    for index, chapter in enumerate(chapters):

        iserror = chapter_retrieve(chapter, 'cbz', kivy_object.ids.directory.text)

        if iserror:
            error_chapters.append(iserror)

        print('Progress')
        kivy_object.ids.download_progress.value += 1

    kivy_object.ids.download_status.text = 'Download Complete!'
    kivy_object.ids.batch_download.disable = False
    kivy_object.ids.directory.readonly = False
    kivy_object.ids.url.readonly = False



class ProgramWindow(Widget):

    def start_download(self):

        try:
            quicktest = BeautifulSoup(requests.get(self.ids.url.text).text, 'lxml')
            chapter_frame_test1 = quicktest.find('ul', {'class':'row-content-chapter'})
            chapter_frame_test2 = quicktest.find('div', {'class':'chapter-list'})
        except:
            self.ids.url.text = 'Wrong url!'
            return

        if chapter_frame_test1 == None and chapter_frame_test2 == None:
            self.ids.url.text = 'Wrong url!'
            return

        if not os.path.exists(self.ids.directory.text):
            self.ids.directory.text = 'Wrong directory!'
            return
        else:
            if self.ids.directory.text[-1] == '\\':
                self.ids.directory.text = self.ids.directory.text[:-1]

        t = Thread(target=downloader, args=(self, ))
        t.daemon = True
        t.start()

        



class Application(App):
    def build(self):
        self.title = 'Azusa - Manga Downloader'
        return ProgramWindow()


if __name__ == '__main__':
    Application().run()
