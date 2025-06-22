import instaloader
import os
import shutil
from pathlib import Path


def url_to_postcode(url):
    postcode = ""
    try:
        url = url.replace("https://www.instagram.com/", "")
        postcode = url[url.index("/")+1:]
        postcode = postcode[:postcode.index("/")]
    except Exception as e:
        print(f"error : {url}: {e} ")
    return postcode


def download_post(postcode, output_path="download"):
    L = instaloader.Instaloader()
    try:
        print(os.getcwd())
        post = instaloader.Post.from_shortcode(L.context, postcode)
        if os.getcwd().find("downloads\\instagram") == -1:
            os.chdir("downloads\\instagram")
        print(os.getcwd())
        L.download_post(post, target="insta_" + postcode)
        path = path_post(postcode)
        print(
            f"Reel with postcode '{postcode}' downloaded successfully to '{output_path}'")
        return path
    except Exception as e:
        print(f"Error downloading reel with postcode '{postcode}': {e}")
        return


def path_post(postcode):
    postpath = "insta_" + postcode
    path = None
    if postpath in os.listdir():
        try:
            os.chdir(postpath)
            files_list = os.listdir()
            if ".mp4" in files_list[2] and os.statvfs(files_list[2]):
                path = Path(os.getcwd() + "\\" + files_list[2])
            elif ".jpg" in files_list[0]:
                path = Path(os.getcwd() + "\\" + files_list[0])
            os.chdir("../")
            return path
        except Exception as e:
            print(f"Error path with postcode '{postcode}': {e}")


def delete_post(postcode):
    postcode = "insta_" + postcode
    if postcode in os.listdir():
        try:
            shutil.rmtree(postcode)
            return True
        except Exception as e:
            print(f"Not delete error : {e}")
            return False
    else:
        print("no file found")
