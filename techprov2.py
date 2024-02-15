from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import random
import os
import re

#get url with a simple user agent fake 
def get_url(url):
    user_agents_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        ]
    r = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
    return r.text

#rechercher un mot sur freepik
def research(*words):
    freepik = "https://fr.freepik.com/search?ai=exclude&format=search&page=1&query="
    freepik += f'{"%20".join(words)}&type=photo'
    return freepik

#class link
class link:
    """description de la classe"""     
    def __init__(self, url):
     self.url = url
     self.html = BeautifulSoup(get_url(self.url), 'html.parser')

    #scrap images and return the name of one class
    def selectionneur(self, number):
        try:
            pic_html = self.html.find_all('img')[number]['class']
            return pic_html
        except:
            pic_html = ["no class name"]
        return pic_html
    
    #create a list of all class thanks to selectionneur
    def c_list(self, n):
        names_list = []
        for i in range(n):
         if self.selectionneur(i)[0] not in names_list:
             names_list.append(self.selectionneur(i)[0])
        return names_list

    #get the picture url
    def get_picture(self, class_name, image_number = 0):
        soup = self.html
        picture = soup.find_all('img', {'class': class_name})[image_number]['data-src']
        return picture
    
    #return a list of pictures url
    def url_list(self, class_name="lzy"):
        soup = self.html
        img_list = soup.find_all('img', {f'class': {class_name}})
        url_list = [img['data-src'] for img in img_list if 'data-src' in img.attrs]
        return url_list
    
    #selectionner une page sur fr.freepik.com 
    def page_selection(self, page=1):
        p_url = re.sub(r'page=[^&]+', f'page={page}', self.url)
        return link(p_url)
    
    #liste des urls de page 
    def page_list(self, num:int):
        p_list = [self.page_selection(page=i+1).url for i in range(num)]
        return p_list
    
    def num_list(self, num=60):
        page = self.url_list()
        p=1
        
        while len(page) < num:
                p+=1
                page += self.page_selection(p).url_list()
        
        return page[0:num]

#create a path directory 
def load_path(dirname:str):
     path = os.path.join(os.getcwd(), 'album//', dirname) 
     if not os.path.exists(path):
         os. makedirs(path)
     return path

#downloader
def download_image(url, dirname, file_name):
    direction = load_path("_".join(dirname))
    with open(os.path.join(direction, f"{file_name}.jpg"), "wb+") as folder:
        folder.write(requests.get(url).content) 

#télécharger toute la page 
def download_page(url_list, dirname, file_name):
    for i, url in enumerate(url_list):
        download_image(url, dirname, f"{file_name}{i}")

#test = link(research(*["chat","seul"]))
#len(test.num_list(66))

def create_tag(category, sample_size):
    tag_title = category.capitalize()
    i = sample_size
    nb_pictures = f"{i} Pictures"  
    
    pic_icon = Image.open(f"album/{category}/{category}1.jpg")       
    icon = pic_icon.resize((75,75))
    icon = icon.convert("RGBA")
    
    # Get rounded corners    
    mask = Image.new('L', icon.size, 0)
    draw = ImageDraw.Draw(mask)
    left, top, right, bottom = 0, 0, icon.size[0], icon.size[1]
    # Draw four rectangles to fill the area outside the rounded corners
    # The corners will remain 0 (transparent), and the rest will be 255 (opaque)
    draw.rounded_rectangle((left, top, right, bottom), radius=15, fill=255)
    # Apply the mask to give the image rounded corners
    rounded_image = ImageOps.fit(icon, mask.size, centering=(0.5, 0.5))
    rounded_image.putalpha(mask)
    icon = rounded_image
    
    #Fusion template + image
    album_tag = Image.open('static/images/blank_class.png')
    album_tag = album_tag.convert("RGBA")
    album_tag.paste(icon, (12, 8), icon)
    
    #Write infos on tag
    I1 = ImageDraw.Draw(album_tag)
    myFont_class = ImageFont.truetype('static/font/Georgia.ttf', 36)
    myFont_count = ImageFont.truetype('static/font/Georgia.ttf', 22)
    I1.text((105,7), tag_title, font=myFont_class, fill=(41, 41, 41))
    I1.text((113,52), nb_pictures, font=myFont_count, fill=(41, 41, 41))
    if not os.path.exists("static//images//tags"):
        os. makedirs("static//images//tags")
    album_tag.save(f"static/images/tags/{category}_tag.png", format="png")
    #album_tag.show()
    
def get_tags():
    image_directory = 'static/images/tags'
    image_urls = [os.path.join(image_directory, filename) for filename in os.listdir(image_directory) if filename.endswith(('.png', '.jpg', '.jpeg'))]        
    return image_urls
