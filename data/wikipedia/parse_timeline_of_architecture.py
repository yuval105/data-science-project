import bs4
import requests
from multiprocessing import Pool
import re

WIKIPEDIA = 'https://en.wikipedia.org'

def text_to_year(text:str):
    if text.isnumeric():
        return int(text)

    if text.strip()[-1] == 's':
        s = text.strip()[:-1]
        if s.isnumeric():
            return int(s)

    return -1

def parse_period_architecture_page(page):
    year, link = page
    link = WIKIPEDIA + link
    r = requests.get(link)
    bs = bs4.BeautifulSoup(r.content, 'html.parser')
    span = bs.find('span', {'id': re.compile('^Buildings')})
    ul  = span.find_next('ul') # this ul contains all the buildings
    current_year = year
    buildings = []
    for li in ul.find_all('li'):
        nums = re.search('[0-9]+', str(li))
        if nums is not None:
            new_year = int(re.search('[0-9]+', str(li)).group())
            if new_year != 1 and new_year > current_year:
                current_year = new_year

        link = li.find('a')
        if link:
            buildings.append((year, link['href']))

    return buildings

def parse_all_period(period_pages, number_of_workers=None):
    with Pool(number_of_workers) as p:
        return p.map(parse_period_architecture_page, period_pages)


def parse_timeline_of_architecture():
    '''
    Returns:
        1. a list of (link, year) for pages like https://en.wikipedia.org/wiki/1560s_in_architecture
    '''

    link = WIKIPEDIA + '/wiki/Timeline_of_architecture'
    r = requests.get(link)
    bs = bs4.BeautifulSoup(r.content, 'html.parser')
    all_periods = bs.find_all('ul')
    result = []
    for period in all_periods:
        for line in period.find_all('li'):
            if type(line) != bs4.element.Tag or line.has_attr('class'):
                continue

            link = line.find_next('a')
            if 'BC' in link.text:
                return result # don't want to deal with bc years

            year = text_to_year(link.text)
            if 'architecture' in link['href'] and 0 <= year <= 1850:
                result.append((year, link['href']))

    return result


if __name__ == '__main__':
    r = parse_timeline_of_architecture()
    buildings = parse_all_period(r)
    pass

