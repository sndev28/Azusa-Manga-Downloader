

                                             ###############################################################################
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                 AZUSA                                       #
                                             #                                                                             #
                                             #                        VERSION CODE : 4.00.00                               #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             ###############################################################################






## Important infos
# 1. To add support for new sites, new module for new site with chapter retriever, add meta creator in helpers, chapter loop in
#    downloader and urlchecker in the order : helpers.chapter_list_generator -> site.py.chapter_meta_creator -> downloader add entry -> 
#    site.py.chapter_retriever -> urlchecker
#
#
#
##




import requests
from os import path, system
from bs4 import BeautifulSoup
from threading import Thread
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import sys
import multiprocessing


#Helper modules

from retrievers.urlchecker import urlchecker
from retrievers.helpers import chapter_list_generator
from retrievers.downloader import downloader
from retrievers.py_exe import resource_path


#version code
version_code = '4.00.00'

#Runner


def main():

    multiprocessing.freeze_support()
    
    from kivymd.app import MDApp
    from kivy.lang import Builder
    from kivy.core.window import Window
    from kivy.clock import Clock
    from kivy.core.audio import SoundLoader
    from kivy.resources import resource_add_path, resource_find


    if hasattr(sys, '_MEIPASS'):
        resource_add_path(path.join(sys._MEIPASS))

    Window.size = (950,750)

    # Builder.load_file(resource_path('azusa.kv'))
    alert = SoundLoader.load(resource_path('alert.mp3'))



    class Application(MDApp):

        

        def start_download(self):

            print("Starting process!")

            self.root.ids.batch_download.disabled = True  #disables button to prevent extra initialization
            self.root.ids.download_status.text = 'Initializing Download...Please wait!'
            self.root.ids.download_progress.value = 0
            self.root.ids.directory.readonly = True
            self.root.ids.url.readonly = True
            self.root.ids.cancel_download.disabled = False
            self.root.ids.serialize_check.disabled = True

            

            t = Thread(target=self.download_initializer)
            t.daemon = True
            t.start()

        def download_initializer(self):

            t1 = time.perf_counter()

            if self.root.ids.url.text == '':
                self.root.ids.url.helper_text = 'Empty url!'
                self.root.ids.url.error = True
                self.root.ids.download_status.text = 'Empty url!'
                self.root.ids.batch_download.disabled = False #renables button due to error
                self.root.ids.directory.readonly = False
                self.root.ids.url.readonly = False
                self.root.ids.cancel_download.disabled = True
                self.root.ids.serialize_check.disabled = False
                return

            elif self.root.ids.directory.text == '':
                self.root.ids.directory.helper_text = 'Empty directory!'
                self.root.ids.directory.error = True
                self.root.ids.download_status.text = 'Empty directory!'
                self.root.ids.batch_download.disabled = False #renables button due to error
                self.root.ids.directory.readonly = False
                self.root.ids.url.readonly = False
                self.root.ids.cancel_download.disabled = True
                self.root.ids.serialize_check.disabled = False
                return


            try:
                test = BeautifulSoup(requests.get(self.root.ids.url.text).text, 'lxml')
            except:
                self.root.ids.url.error = True
                self.root.ids.url.helper_text = 'Invalid url!'
                self.root.ids.batch_download.disabled = False #renables button due to error
                self.root.ids.directory.readonly = False
                self.root.ids.url.readonly = False
                self.root.ids.cancel_download.disabled = True
                self.root.ids.serialize_check.disabled = False
                self.root.ids.download_status.text = 'Download not started yet!'
                return

            if not urlchecker(self.root.ids.url.text):
                self.root.ids.url.error = True
                self.root.ids.url.helper_text = 'Unsupported site!'
                self.root.ids.batch_download.disabled = False #renables button due to error
                self.root.ids.directory.readonly = False
                self.root.ids.url.readonly = False
                self.root.ids.cancel_download.disabled = True
                self.root.ids.serialize_check.disabled = False
                self.root.ids.download_status.text = 'Download not started yet!'
                return

            if not path.exists(self.root.ids.directory.text):
                self.root.ids.directory.error = True
                self.root.ids.batch_download.disabled = False #renables button due to error
                self.root.ids.directory.readonly = False
                self.root.ids.url.readonly = False
                self.root.ids.cancel_download.disabled = True
                self.root.ids.serialize_check.disabled = False
                self.root.ids.download_status.text = 'Download not started yet!'
                return
            else:
                if self.root.ids.directory.text[-1] == '\\':
                    self.root.ids.directory.text = self.root.ids.directory.text[:-1]

            
            #Pacman gif starts
            self.root.ids.gif.opacity = 1


            downloader(self, self.serialize_flag)
            alert.play()

            #uncomment to view execution time details
            total_download_time = time.perf_counter() - t1
            print('Execution time = ', total_download_time,'s')
            self.root.ids.download_status.text += f' Total time taken = {time.strftime("%H:%M:%S", time.gmtime(total_download_time))}'

        def updater_button(self):
            pool = ThreadPoolExecutor(max_workers=1)
            pool.submit(self.updater)

        def updater(self):

            self.root.ids.download_status.text = 'Checking for update!'
            new_version_code = requests.get('https://drive.google.com/uc?export=download&id=1BKHZ1c_S6xVWwf_LE_prBqGa8X3M6BVH').text

            if new_version_code != version_code:
                self.root.ids.download_status.text = 'Downloading update!'
                update_link = requests.get('https://drive.google.com/uc?export=download&id=1WJaXgcxv2tnn0WCtXiHjLQCET5c10bF_').text

                self.root.ids.gif.opacity = 1

                download = requests.get(update_link)

                with open(f'Azusa_{new_version_code}.exe', 'wb') as file:
                    CHUNK_SIZE = 524288
                    for chunk in download.iter_content(CHUNK_SIZE):
                        file.write(chunk)


                self.root.ids.download_status.text = 'Updating!'

                self.root.ids.gif.opacity = 0

                self.root.ids.download_status.text = 'Please restart the application! Delete the older version!'
                

            else:
                self.root.ids.download_status.text = 'No available update!'


        def cancel_download(self):
            sys.exit(0)

        serialize_flag = False

        def serialize(self):
            if self.root.ids.serialize_check.current:
                self.serialize_flag = self.root.ids.serialize_check.current = False
                self.root.ids.serialize_check.md_bg_color = 1,1,1,1
                self.root.ids.serialize_check.text_color = self.theme_cls.primary_color

            else:
                self.serialize_flag = self.root.ids.serialize_check.current = True
                self.root.ids.serialize_check.md_bg_color = self.theme_cls.primary_color
                self.root.ids.serialize_check.text_color = 1,1,1,1

            print(self.serialize_flag)


        def build(self):
            self.theme_cls.primary_palette = "Green"
            self.theme_cls.theme_style = "Light"
            self.title = 'Azusa - Manga Downloader'
            self.root = Builder.load_file(resource_path('azusa.kv'))

        


    Application().run()


if __name__ == '__main__':
    main()
    
