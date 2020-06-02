import bs4
import requests

WIKIPEDIA = 'https://en.wikipedia.org/wiki/'

def text_to_year(text:str):
    if text.isnumeric():
        return int(text)

    if text.strip()[-1] == 's':
        s = text.strip()[:-1]
        if s.isnumeric():
            return int(s)

    return -1


def parse_timeline_of_architecture():
    '''
    Returns:
        1. a list of (link, year) for pages like https://en.wikipedia.org/wiki/1560s_in_architecture
    '''

    link = WIKIPEDIA + 'Timeline_of_architecture'
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
    for i in r:
        print(i)

