

                                             ###############################################################################
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                 AZUSA                                       #
                                             #                                                                             #
                                             #                        VERSION CODE : 2.74.69                               #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             #                                                                             #
                                             ###############################################################################



## Important infos
# 1. To add support for new sites, new module for new site with chapter retriever, add meta creator in helpers, chapter loop in
#    downloader and urlchecker
#
#
#
##



from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

import requests
from os import path
from bs4 import BeautifulSoup
from threading import Thread


#Helper modules

from retrievers.urlchecker import urlchecker
from retrievers.helpers import chapter_list_generator
from retrievers.downloader import downloader

#Runner

Window.size = (900,660)


Builder.load_file('azusa.kv')



class ProgramWindow(Widget):

    def start_download(self):

        self.ids.batch_download.disable = True  #disables button to prevent extra initialization

        try:
            test = BeautifulSoup(requests.get(self.ids.url.text).text, 'lxml')
        except:
            self.ids.url.text = 'Invalid url!'
            self.ids.batch_download.disable = False #renables button due to error
            return

        if not urlchecker(test):
            self.ids.url.text = 'Unsopported site!'
            self.ids.batch_download.disable = False #renables button due to error
            return

        if not path.exists(self.ids.directory.text):
            self.ids.directory.text = 'Invalid directory!'
            self.ids.batch_download.disable = False #renables button due to error
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
