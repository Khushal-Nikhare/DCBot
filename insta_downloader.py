import instaloader
import os
import shutil
from pathlib import Path

L = instaloader.Instaloader()

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
    
    original_dir = os.getcwd()
    
    try:
        print(f"Starting download from: {os.getcwd()}")
        
        # Create downloads directory if it doesn't exist
        download_dir = os.path.join(original_dir, "downloads", "instagram")
        os.makedirs(download_dir, exist_ok=True)
        os.chdir(download_dir)
        
        print(f"Changed to download directory: {os.getcwd()}")
        
        # Download the post
        post = instaloader.Post.from_shortcode(L.context, postcode)
        L.download_post(post, target="insta_" + postcode)
        
        # Get the file path
        path = path_post(postcode)
        
        if path:
            print(f"Post with postcode '{postcode}' downloaded successfully")
            return path
        else:
            print(f"Failed to locate downloaded file for postcode '{postcode}'")
            return None
            
    except Exception as e:
        print(f"Error downloading post with postcode '{postcode}': {e}")
        return None
    finally:
        # Always return to original directory
        os.chdir(original_dir)


def path_post(postcode):
    postpath = "insta_" + postcode
    current_dir = os.getcwd()
    
    try:
        if postpath in os.listdir():
            post_dir = os.path.join(current_dir, postpath)
            files_list = os.listdir(post_dir)
            
            # Look for video files first, then images
            for file in files_list:
                if file.endswith(('.mp4', '.mov', '.avi')):
                    return os.path.join(post_dir, file)
            
            # If no video found, look for images
            for file in files_list:
                if file.endswith(('.jpg', '.jpeg', '.png')):
                    return os.path.join(post_dir, file)
                    
            print(f"No suitable media files found in {postpath}")
            return None
        else:
            print(f"Directory {postpath} not found")
            return None
            
    except Exception as e:
        print(f"Error finding path for postcode '{postcode}': {e}")
        return None


def delete_post(postcode):
    try:
        # Look for the post directory in downloads/instagram
        download_dir = os.path.join(os.getcwd(), "downloads", "instagram")
        postpath = os.path.join(download_dir, "insta_" + postcode)
        
        if os.path.exists(postpath):
            shutil.rmtree(postpath)
            print(f"Deleted post directory: {postpath}")
            return True
        else:
            print(f"Post directory not found: {postpath}")
            return False
    except Exception as e:
        print(f"Error deleting post: {e}")
        return False
