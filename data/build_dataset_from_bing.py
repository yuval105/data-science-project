from csv import DictReader
import download_bing_images
import os

CSV_FILE = 'architectural_styles.csv'

def build_dir_tree(csv_file):
    with open(csv_file, 'r') as f:
        csv = DictReader(f)
        for line in csv:
            if line['id'] != '':
                dir_path = os.path.join('images', line['class'], line['subclass'], line['subclass2'])
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)


def download_images(csv_file, images_per_class=200):
    with open(csv_file, 'r') as f:
        csv = DictReader(f)
        for line in csv:
            if line['id'] != '':
                dir_path = os.path.join('images', line['class'], line['subclass'], line['subclass2'])
                finest_class = line['subclass2'] if line['subclass2'] != '' else \
                    line['subclass'] if line['subclass'] != '' else line['class']
                print(f'downloading from bing: {finest_class}')
                # the script tends to fail on some images and then succeed
                download_bing_images.main(['-s', f'{finest_class} architecture', '-o', dir_path, '--limit', f'{images_per_class}'])
                additional_terms = line['additional search terms'].split(',')
                for term in additional_terms:
                    if term != '':
                        download_bing_images.main(['-s', f'{term} architecture', '-o', dir_path, '--limit', f'{images_per_class}'])


def main():
    build_dir_tree(CSV_FILE)
    download_images(CSV_FILE)


if __name__ == '__main__':
    main()
