from duckduckgo_search import DDGS, AsyncDDGS
import requests, os
from PIL import Image
from io import BytesIO

def download_image(url, save_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image.save(save_path)
        print("Image downloaded and verified successfully!")
    except Exception as e:
        print(f"Error downloading or verifying image: {e}")

# results = DDGS().images('python', max_results=5)
def get_image(topic, count):
    results = DDGS().images(topic, region='wt-wt', safesearch='off', max_results=20)
    i = 0
    paths = []
    for image in results:
        try:
            url = image['image']
            folder = topic.replace(' ','-')
            if not os.path.exists('output/images'):
                os.system(f'mkdir output/images')
            if not os.path.exists(f'output/images/{folder}'):
                os.system(f'mkdir output/images/{folder}')

            extension = url.split('.')[-1]
            extension = extension.split('?')[0]
            path = f'output/images/{folder}/image{i}.{extension}'
            i += 1
            download_image(url, path)
            paths.append(path)
            print(paths)
        except Exception as e:
            print(f"Error downloading image: {e}")
        if i == count:
            break
    
    return paths

def get_image_links(topic, count):
    results = []
    try:
        results = DDGS().images(topic, region='wt-wt', safesearch='off', max_results=20)
    except Exception as e:
        print(f"Error fetching image link: {e}")
    i = 0
    links = []
    for image in results:
        try:
            url = image['image']
            links.append(url)
            i += 1
        except Exception as e:
            print(f"Error fetching image link: {e}")
        if i == count:
            break
    
    return links