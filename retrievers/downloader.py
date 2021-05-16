import os
import concurrent.futures
from pebble import ProcessPool

#helper functions

from retrievers.helpers import chapter_list_generator
import retrievers.mangakakalot as mangakakalot
import retrievers.bato as bato


#Runner

def downloader(kivy_object, serialize_flag, **kwargs):

    cwd = os.getcwd()

    site_url = kivy_object.ids.url.text

    all_chapters = chapter_list_generator(site_url)  

    all_chapters.reverse()

    try:
        if kwargs['mode'] == 'selected':
            chapters = [all_chapters[index] for index, checkbox in enumerate(kwargs['checklist']) if checkbox.active == True]  #return list of active chapterss
        else:
            chapters = all_chapters
    except:
        chapters = all_chapters

    no_of_chapters = len(chapters)
    no_of_workers = int(kivy_object.ids.cpu_count.text)   #no of parallel downloads
    print("Number of parellel worker = ", no_of_workers)
    kivy_object.ids.download_progress.max = no_of_chapters

    




    #site-wise chapter downloader                      ADD SUPPORT FOR NEW SITES HERE



    if 'manganelo' in site_url or 'mangakakalot' in site_url:               #Mangakakalot or Manganelo

        with ProcessPool(max_workers=no_of_workers) as processes:
            processing = [processes.schedule(mangakakalot.chapter_retrieve, args=(chapter, kivy_object.ids.directory.text, index, serialize_flag)) for index, chapter in enumerate(chapters)]
            
            for _ in concurrent.futures.as_completed(processing):
                kivy_object.ids.download_progress.value += 1     #Progress bar update
                # print(_)     #used to print errors in multiprocessing thread

        # sequential downloads
        # for chapter in chapters:
        #     mangakakalot.chapter_retrieve(chapter, kivy_object.ids.directory.text)

            



    elif 'bato' in site_url:                                                #Bato.to

        with concurrent.futures.ProcessPoolExecutor(max_workers=no_of_workers) as processes:
            processing = [processes.schedule(bato.chapter_retrieve, args=(chapter, kivy_object.ids.directory.text, index, serialize_flag)) for index, chapter in enumerate(chapters)]
            
            for _ in concurrent.futures.as_completed(processing):
                kivy_object.ids.download_progress.value += 1     #Progress bar update
                # print(_)     #used to print errors in multiprocessing thread
                

        # sequential downloads
        # for chapter in chapters:
        #     bato.chapter_retrieve(chapter, kivy_object.ids.directory.text)





