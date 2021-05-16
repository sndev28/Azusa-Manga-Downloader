

                                             ###############################################################################
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                 AZUSA                                       #
                                             #                                                                             #
                                             #                        VERSION CODE : 3.87.54                               #
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
from concurrent.futures import ThreadPoolExecutor
import sys
import multiprocessing


#Helper modules

from retrievers.urlchecker import urlchecker
from retrievers.downloader import downloader
from retrievers.py_exe import resource_path


#version code
version_code = '3.87.54'

#Runner


def main():

    multiprocessing.freeze_support()
    
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.lang import Builder
    from kivy.core.window import Window
    from kivy.clock import Clock
    from kivy.core.audio import SoundLoader
    from kivy.resources import resource_add_path, resource_find

    if hasattr(sys, '_MEIPASS'):
        resource_add_path(path.join(sys._MEIPASS))

    Window.size = (950,750)

    Builder.load_file(resource_path('azusa.kv'))
    alert = SoundLoader.load(resource_path('resources\\alert.mp3'))



    class ProgramWindow(Widget):

        

        def start_download(self):

            print("Starting process!")

            self.ids.batch_download.disabled = True  #disables button to prevent extra initialization
            self.ids.download_status.text = 'Initializing Download...Please wait!'
            self.ids.download_progress.value = 0
            self.ids.directory.readonly = True
            self.ids.url.readonly = True
            self.ids.cpu_count.readonly = True
            self.ids.cancel_download.disabled = False
            self.ids.serialize_check.disabled = True

            

            self.t = Thread(target=self.download_initializer)
            self.t.daemon = True
            self.t.start()

        def download_initializer(self):

            t1 = time.perf_counter()

            try:
                test = BeautifulSoup(requests.get(self.ids.url.text).text, 'lxml')
            except:
                self.ids.url.text = 'Invalid url!'
                self.ids.batch_download.disabled = False #renables button due to error
                self.ids.directory.readonly = False
                self.ids.url.readonly = False
                self.ids.cpu_count.readonly = False
                self.ids.cancel_download.disabled = True
                self.ids.serialize_check.disabled = False
                self.ids.download_status.text = 'Download not started yet!'
                return

            if not urlchecker(self.ids.url.text):
                self.ids.url.text = 'Unsupported site!'
                self.ids.batch_download.disabled = False #renables button due to error
                self.ids.directory.readonly = False
                self.ids.url.readonly = False
                self.ids.cpu_count.readonly = False
                self.ids.cancel_download.disabled = True
                self.ids.serialize_check.disabled = False
                self.ids.download_status.text = 'Download not started yet!'
                return

            if not path.exists(self.ids.directory.text):
                self.ids.directory.text = 'Invalid directory!'
                self.ids.batch_download.disabled = False #renables button due to error
                self.ids.directory.readonly = False
                self.ids.url.readonly = False
                self.ids.cpu_count.readonly = False
                self.ids.cancel_download.disabled = True
                self.ids.serialize_check.disabled = False
                self.ids.download_status.text = 'Download not started yet!'
                return
            else:
                if self.ids.directory.text[-1] == '\\':
                    self.ids.directory.text = self.ids.directory.text[:-1]

            
            #Pacman gif starts
            self.ids.gif.opacity = 1

            
            self.ids.download_status.text = 'Downloading under progress!'

            downloader(self, self.serialize_flag)
            alert.play()
            print('All done!')
            self.ids.download_status.text = 'Download Complete!'
            self.ids.batch_download.disable = False
            self.ids.directory.readonly = False
            self.ids.url.readonly = False
            self.ids.cpu_count.readonly = False
            self.ids.cancel_download.disabled = True
            self.ids.serialize_check.disabled = False
            self.ids.gif.opacity = 0

            #uncomment to view execution time details
            total_download_time = time.perf_counter() - t1
            print('Execution time = ', total_download_time,'s')
            self.ids.download_status.text += f' Total time taken = {time.strftime("%H:%M:%S", time.gmtime(total_download_time))}'

        def updater_button(self):
            pool = ThreadPoolExecutor(max_workers=1)
            pool.submit(self.updater)

        def updater(self):


            self.ids.download_status.text = 'Checking for update!'
            new_version_code = requests.get('https://drive.google.com/uc?export=download&id=1BKHZ1c_S6xVWwf_LE_prBqGa8X3M6BVH').text

            if new_version_code != version_code:
                self.ids.download_status.text = 'Downloading update!'
                update_link = requests.get('https://drive.google.com/uc?export=download&id=1WJaXgcxv2tnn0WCtXiHjLQCET5c10bF_').text

                self.ids.gif.opacity = 1

                download = requests.get(update_link)

                with open(f'Azusa_{new_version_code}.exe', 'wb') as file:
                    CHUNK_SIZE = 524288
                    for chunk in download.iter_content(CHUNK_SIZE):
                        file.write(chunk)


                self.ids.download_status.text = 'Updating!'

                self.ids.gif.opacity = 0

                self.ids.download_status.text = 'Please restart the application! Delete the older version!'
                

            else:
                self.ids.download_status.text = 'No available update!'


        def cancel_download(self):
            sys.exit(0)

            
        serialize_flag = False
        
        def serialize(self, instance, value):
            self.serialize_flag = value
            print(self.serialize_flag)

        def cpu_counter(self, *args):
            self.ids.cpu_count.text = str(args[1])


        
        





            



    class Application(App):
        def build(self):
            self.title = 'Azusa - Manga Downloader'
            return ProgramWindow()


    Application().run()


if __name__ == '__main__':
    main()
    
