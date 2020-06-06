import bs4
import requests
from multiprocessing import Pool
import geocoder
import csv

WIKIPEDIA = 'https://en.wikipedia.org'

def build_arch_style():
    '''
    Builds dictionary that maps from word to style
    '''
    arch_style = {}
    reader = csv.DictReader(open('../architectural_styles.csv', 'r'))
    for line in reader:
        if line['class'].strip() == '':
            continue

        clas = line['class'].strip()
        subclass = line['subclass'].strip()
        subclass2 = line['subclass2'].strip()

        arch_style[line['class']] = clas
        finest_class = clas
        if subclass != '':
            arch_style[line['subclass']] = subclass
            finest_class = subclass
        if subclass2 != '':
            arch_style[line['subclass2']] = subclass2
            finest_class = subclass2

        if line['additional search terms'].strip() != '':
            search_terms = line['additional search terms'].strip().split(',')
            for term in search_terms:
                arch_style[term] = finest_class

    return arch_style


arch_style = build_arch_style()


def get_known_arch_style(styles):
    all_styles = styles.split(',')
    for style in all_styles:
        s = style.strip()
        if s in arch_style.keys():
            return arch_style[s]

    return ''


def get_location(name):
    '''
    return lattitue, longitude, score
    '''
    try:
        g = geocoder.arcgis(name)
        if not g.ok:
            return 0, 0, 0
        properties = g.geojson['features'][0]['properties']
        return properties['lat'], properties['lng'], properties['score']
    except:
        pass
        return 0, 0, 0


def parse_page(page):
    year, link = page
    # return thumbnails and full images
    r = requests.get(WIKIPEDIA + link)
    bs = bs4.BeautifulSoup(r.content, 'html.parser')

    title = bs.find('h1', {'id':'firstHeading'}).text

    side_box = bs.find('table', {'class':'infobox vcard'})
    style = ''
    if side_box is not None:
        arch = side_box.find('th', string='Style')
        is_style_found = arch is not None
        if is_style_found:
            style = arch.find_next('td').text

    known_style = get_known_arch_style(style)

    # find all the iamges
    thumbnails = []
    full_images = []
    for img in bs.find_all('a', {'class':'image'}):
        i = img.find('img')
        thumbnails.append((i['src']))
        full_images.append(img['href'])

    loc = get_location(title) # get location
    return {'title': title, 'year': year, 'link': link, 'style': style, 'known_style': known_style, 'thumbnails': thumbnails,
            'images': full_images, 'lat': loc[0], 'lng': loc[1], 'loc_score': loc[2]}

def parse_pages(pages, threads=None):
    '''
    Parse pages, and for each return a dict
    pages - a list of (year, link)
    '''

    p = Pool(threads)
    return p.map(parse_page, pages)



if __name__ == '__main__':
    res = parse_page((1000, '/wiki/Odda%27s_Chapel'))
    get_location(res['title'])
    print(res)
