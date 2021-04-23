from bs4 import BeautifulSoup
import requests


def num_to_fourdigit(num):

    if len(str(num)) == 1:
        return f'000{num}'

    elif len(str(num)) == 2:
        return f'00{num}'

    elif len(str(num)) == 3:
        return f'0{num}'

    elif len(str(num)) == 4:
        return str(num)


def chapter_list_generator(site_url):


    ##    ADD SUPPORT FOR NEW SITES HERE

    if 'manganelo' in site_url or 'mangakakalot' in site_url:
        
        from retrievers.mangakakalot import chapter_meta_creator
        return chapter_meta_creator(site_url)
    
    else:
        return None