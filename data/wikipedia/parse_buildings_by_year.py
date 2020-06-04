import bs4
import requests
from multiprocessing import Process, Queue, Pool
import multiprocessing
import re

WIKIPEDIA = 'https://en.wikipedia.org'

def search_page(year, link):
    '''
    Returns pages and categories
    '''

    r = requests.get(WIKIPEDIA + link)
    print(WIKIPEDIA + link)
    bs = bs4.BeautifulSoup(r.content, 'html.parser')
    subs = bs.find('div', {'id': 'mw-subcategories'})

    categories = []
    if subs is not None:
        real_subs = subs.find('div', {'class':'mw-content-ltr'})
        links = real_subs.find_all('a')
        for l in links:
            categories.append(l['href'])

    pages_in = []
    pages = bs.find('div', {'id': 'mw-pages'})
    if pages is not None:
        only_pages = pages.find('div', {'class':'mw-content-ltr'})
        for l in only_pages.find_all('a'):
            pages_in.append(l['href'])

    return categories, pages_in

def search_thread(queue:Queue, pages_queue:Queue):
    global found_pages
    while not queue.empty():
        year, link = queue.get(block=True)
        cats, pages = search_page(year, link)
        for cat in cats:
            queue.put((year, cat), block=True)

        [pages_queue.put((year, i)) for i in pages]

def main(first_year, last_year):
    pool = multiprocessing.Pool(processes=1)
    m = multiprocessing.Manager()
    q = m.Queue()
    pages_queue = m.Queue()
    [q.put((year, f'/wiki/Category:Buildings_and_structures_completed_in_{year}')) for year in range(first_year, last_year)]
    workers = pool.apply(search_thread, (q, pages_queue))
    return pages_queue



if __name__ == '__main__':
    pages = main(1001, 1015)
    while not pages.empty():
        print(pages.get(block=True))



