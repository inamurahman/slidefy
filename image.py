import requests
from bs4 import BeautifulSoup
from PIL import Image

def getdata(url):
    r = requests.get(url)
    return r.text

def search_images(topic):
    link="https://www.google.co.in/search?q="+topic+"&source=lnms&tbm=isch"
    link="https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"%(topic)
    #link = f"https://www.google.com/search?q={topic}"
    htmldata = getdata(link)
    soup = BeautifulSoup(htmldata, 'html.parser')
    images = [] 
    
    for item in soup.find_all('img'): 
        images.append(item['src'])

    return images


def save_image(subject):
    subject = '+'.join(subject.split(' '))
    url = search_images(subject)[1]
    print(url)
    data = requests.get(url).content 
    f = open(f'{subject}.jpg','wb')
    f.write(data) 
    f.close()
    img = Image.open(f'{subject}.jpg') 
    img.show()

