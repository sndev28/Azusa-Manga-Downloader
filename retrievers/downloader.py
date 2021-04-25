import os
import concurrent.futures

#helper functions

from retrievers.helpers import chapter_list_generator
import retrievers.mangakakalot as mangakakalot
import retrievers.bato as bato


#Runner

def downloader(kivy_object):

    cwd = os.getcwd()

    kivy_object.ids.download_status.text = 'Downloading under progress!'

    site_url = kivy_object.ids.url.text

    chapters = chapter_list_generator(site_url)           

    no_of_chapters = len(chapters)
    kivy_object.ids.download_progress.max = no_of_chapters

    




    #site-wise chapter downloader                      ADD SUPPORT FOR NEW SITES HERE



    no_of_workers = int(kivy_object.ids.cpu_count.text)   #no of parallel downloads
    print("Number of parellel worker = ", no_of_workers)


    if 'manganelo' in site_url or 'mangakakalot' in site_url:               #Mangakakalot or Manganelo

        with concurrent.futures.ProcessPoolExecutor(max_workers=no_of_workers) as processes:
            processing = [processes.submit(mangakakalot.chapter_retrieve, chapter, kivy_object.ids.directory.text) for chapter in chapters]
            
            for _ in concurrent.futures.as_completed(processing):
                kivy_object.ids.download_progress.value += 1     #Progress bar update

        # sequential downloads
        # for chapter in chapters:
        #     mangakakalot.chapter_retrieve(chapter, kivy_object.ids.directory.text)

            



    elif 'bato' in site_url:                                                #Bato.to

        with concurrent.futures.ProcessPoolExecutor(max_workers=no_of_workers) as processes:
            processing = [processes.submit(bato.chapter_retrieve, chapter, kivy_object.ids.directory.text) for chapter in chapters]
            
            for _ in concurrent.futures.as_completed(processing):
                kivy_object.ids.download_progress.value += 1     #Progress bar update

        # sequential downloads
        # for chapter in chapters:
        #     bato.chapter_retrieve(chapter, kivy_object.ids.directory.text)









    kivy_object.ids.download_status.text = 'Download Complete!'
    kivy_object.ids.batch_download.disable = False
    kivy_object.ids.directory.readonly = False
    kivy_object.ids.url.readonly = False
    kivy_object.ids.cpu_count.readonly = False
    kivy_object.ids.gif.opacity = 0
