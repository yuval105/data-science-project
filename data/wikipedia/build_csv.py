import data.wikipedia.parse_buildings_by_year as get_all_pages
import data.wikipedia.parse_page as parse_page
import csv

if __name__ == '__main__':
    pages = get_all_pages.main(914, 1850)

    pages_list = []
    while not pages.empty():
        pages_list.append(pages.get())

    parsed_data = parse_page.parse_pages(pages_list)
    writer = csv.DictWriter(open('wiki.csv', 'w'), fieldnames=['year', 'link', 'title', 'thumbnails', 'images', 'lat', 'lng', 'loc_score', 'style', 'known_style'])
    writer.writeheader()
    writer.writerows(parsed_data)

