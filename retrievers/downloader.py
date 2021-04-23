import os


#helper functions

from retrievers.helpers import chapter_list_generator
import retrievers.mangakakalot as mangakakalot


#Runner

def downloader(kivy_object):

    cwd = os.getcwd()

    kivy_object.ids.download_status.text = 'Downloading under progress!'
    kivy_object.ids.directory.readonly = True
    kivy_object.ids.url.readonly = True

    if not os.path.exists(f'{cwd}\\temp'):
        os.mkdir(f'{cwd}\\temp')
    os.system(f'del /q {cwd}\\temp\\*')

    error_chapters = []

    site_url = kivy_object.ids.url.text

    chapters = chapter_list_generator(site_url)            

    no_of_chapters = len(chapters)
    kivy_object.ids.download_progress.max = no_of_chapters





    #site-wise chapter downloader                      ADD SUPPORT FOR NEW SITES HERE

    if 'manganelo' in site_url or 'mangakakalot' in site_url:               #Mangakakalot or Manganelo
        for chapter in chapters:
            mangakakalot.chapter_retrieve(chapter, kivy_object.ids.directory.text)
            #Progress bar update
            kivy_object.ids.download_progress.value += 1









    kivy_object.ids.download_status.text = 'Download Complete!'
    kivy_object.ids.batch_download.disable = False
    kivy_object.ids.directory.readonly = False
    kivy_object.ids.url.readonly = False