from fastai.vision import download_images
import os

def download_image_dataset(urls_base,dest,max_workers,force_download=False):
    files_list = []
    for (root,dirs,files) in os.walk(urls_base):
        for file in files:
            src_path = os.path.join(root,file)
            dest_path_dir = os.path.join(dest,os.path.relpath(root,urls_base))
            if not os.path.exists(dest_path_dir):
                os.makedirs(dest_path_dir)
            downloaded_flag_file = os.path.join(dest_path_dir,f".downloaded_{file}")
            if os.path.exists(downloaded_flag_file) and not force_download:
                print(f"{src_path} already downloaded")
            else:
                print(f"Downloading {src_path}")
                download_images(src_path,dest_path_dir,max_workers=max_workers)
                open(downloaded_flag_file,'w').close()
        
