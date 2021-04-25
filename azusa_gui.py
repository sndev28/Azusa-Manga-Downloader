

                                             ###############################################################################
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                 AZUSA                                       #
                                             #                                                                             #
                                             #                        VERSION CODE : 3.42.16                               #
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
from os import path
from bs4 import BeautifulSoup
from threading import Thread
import time



#Helper modules

from retrievers.urlchecker import urlchecker
from retrievers.helpers import chapter_list_generator
from retrievers.downloader import downloader

#Runner


def main():
    
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.lang import Builder
    from kivy.core.window import Window
    from kivy.clock import Clock
    from kivy.core.audio import SoundLoader

    Window.size = (950,700)

    Builder.load_file('azusa.kv')
    alert = SoundLoader.load('alert.mp3')



    class ProgramWindow(Widget):    

        def start_download(self):

            print("Starting process!")

            self.ids.batch_download.disabled = True  #disables button to prevent extra initialization
            self.ids.download_status.text = 'Initializing Download...Please wait!'
            self.ids.download_progress.value = 0
            self.ids.directory.readonly = True
            self.ids.url.readonly = True
            self.ids.cpu_count.readonly = True

            

            t = Thread(target=self.download_initializer)
            t.daemon = True
            t.start()

        def download_initializer(self):

            t1 = time.perf_counter()

            try:
                test = BeautifulSoup(requests.get(self.ids.url.text).text, 'lxml')
            except:
                self.ids.url.text = 'Invalid url!'
                self.ids.batch_download.disable = False #renables button due to error
                self.ids.directory.readonly = False
                self.ids.url.readonly = False
                self.ids.cpu_count.readonly = False
                return

            if not urlchecker(self.ids.url.text):
                self.ids.url.text = 'Unsupported site!'
                self.ids.batch_download.disable = False #renables button due to error
                self.ids.directory.readonly = False
                self.ids.url.readonly = False
                self.ids.cpu_count.readonly = False
                return

            if not path.exists(self.ids.directory.text):
                self.ids.directory.text = 'Invalid directory!'
                self.ids.batch_download.disable = False #renables button due to error
                self.ids.directory.readonly = False
                self.ids.url.readonly = False
                self.ids.cpu_count.readonly = False
                return
            else:
                if self.ids.directory.text[-1] == '\\':
                    self.ids.directory.text = self.ids.directory.text[:-1]

            try:
                int(self.ids.cpu_count.text)

            except:
                if self.ids.cpu_count.text == '0':
                    self.ids.cpu_count.text == '1'

                else:
                    self.ids.cpu_count.text == '4'

            
            #Pacman gif starts
            self.ids.gif.opacity = 1


            downloader(self)
            alert.play()

            #uncomment to view execution time details
            total_download_time = time.perf_counter() - t1
            print('Execution time = ', total_download_time,'s')
            self.ids.download_status.text += f' Total time taken = {time.strftime("%H:%M:%S", time.gmtime(total_download_time))}'



            



    class Application(App):
        def build(self):
            self.title = 'Azusa - Manga Downloader'
            return ProgramWindow()


    Application().run()


if __name__ == '__main__':
    main()
    
