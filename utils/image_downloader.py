from fastai.vision import download_images
from fastai.vision.data import download_image
import os
import pandas as pd
import ast
import requests
from fastai.core import parallel
from functools import partial


def download_image_dataset(urls_base, dest, max_workers, force_download=False):
    files_list = []
    for (root, dirs, files) in os.walk(urls_base):
        for file in files:
            src_path = os.path.join(root, file)
            dest_path_dir = os.path.join(
                dest, os.path.relpath(root, urls_base))
            if not os.path.exists(dest_path_dir):
                os.makedirs(dest_path_dir)
            downloaded_flag_file = os.path.join(
                dest_path_dir, f".downloaded_{file}")
            if os.path.exists(downloaded_flag_file) and not force_download:
                print(f"{src_path} already downloaded")
            else:
                print(f"Downloading {src_path}")
                download_images(src_path, dest_path_dir,
                                max_workers=max_workers)
                open(downloaded_flag_file, 'w').close()


def download_single_image(dest, row, i):
    WIKIPEDIA_URL = "https://en.wikipedia.org/w/api.php"
    images = list(filter(lambda x: x.split(
        '.')[-1].lower() in ['jpg', 'jpeg', 'png'], row))
    if len(images) == 0:
        return (i,None)

    # Get first image_url
    filename = os.path.basename(images[0])
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": filename
    }
    try:
        r = requests.get(WIKIPEDIA_URL, params)
    except Exception as e:
        print(f"Error request {filename} {e}")
        return (i,None)
    data = r.json()
    page = next(iter(data["query"]["pages"].values()))
    if "imageinfo" not in page:
        return (i,None)
    image_info = page["imageinfo"][0]
    image_url = image_info["url"]

    # Download image
    path = os.path.join(dest, filename)
    try:
        download_image(image_url,path)
        return (i,filename)
    except Exception as e:
        print(f"Error request {image_url} {e}")
        return (i,None)



def download_wiki_images(wiki_csv, dest, dest_csv=None, force_download=False, max_rows=None, max_workers=8):
    """
    Download wiki images from the wiki csv. Save a csv with an added column to the path of the image.
    
    """
    dest_csv = dest_csv or os.path.join(dest, 'downloaded.csv')

    def try_convert_to_list(x):
        try:
            r = ast.literal_eval(x)
            return r if isinstance(r, list) else None
        except:
            return None

    if not os.path.exists(dest):
        os.makedirs(dest)
    if os.path.exists(dest_csv) and not force_download:
        df = pd.read_csv(dest_csv)
        df['images'] = df['images'].apply(try_convert_to_list)
        df = df[df['images'].notnull()]
        return df

    df = pd.read_csv(wiki_csv)
    df['images'] = df['images'].apply(try_convert_to_list)
    df = df[df['images'].notnull()]
    if max_rows != None:
        df = df.iloc[:max_rows]
    paths = parallel(partial(download_single_image, dest),
                     df['images'], max_workers=max_workers)
    df['image_path'] = pd.Series(dict(paths)).drop_duplicates()
    df = df[df['image_path'].notnull()]
    df.to_csv(dest_csv,index=False)
    return df
