from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageOps
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import base64
import time 
import os
import re

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 



def get_url(url):
    '''
    Function to retrieve the HTML content of a given URL by using a fake user agent.
    
    Args:
        url (str): The URL to retrieve the content from.
        
    Returns:
        str: The HTML content of the URL.
    '''
    # Crée un objet ChromeOptions
    chrome_options = webdriver.ChromeOptions()

    # Ajoute les arguments pour éviter la notification de Chrome
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--ignore-certificate-errors') # Ignore les erreurs de certificat
    chrome_options.add_argument("--start-maximized")

    driver=webdriver.Chrome(options=chrome_options)
    
    driver.get(url)

    driver.find_element(By.XPATH, """//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button""").click()
    
    # scroll down to the bottom of the page
    while True:

        # instantiate height of webpage 
        last_height = driver.execute_script('return document.body.scrollHeight')

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
 
        # wait for content to load 
        time.sleep(1) 
 
        new_height = driver.execute_script('return document.body.scrollHeight') 
    
        if new_height == last_height: 
            try:   
                driver.find_element(By.XPATH, """//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input""").click()
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                new_height = driver.execute_script('return document.body.scrollHeight') 
                
            except:
                break 
    
        last_height == new_height 

    page_html = driver.page_source

    driver.close()

    return BeautifulSoup(page_html, 'html.parser')


def generate_search_link(*words):
    '''
    Function to generate a search link for google image based on provided keywords.
    
    Args:
        *words (str): Variable number of keyword arguments representing the search terms.
        
    Returns:
        str: A URL link for the search results on google image.
    '''
    return "https://www.google.com/search?q=" + f'{"+".join(words)}+&tbm=isch'
            
class link:
    """
    Class for managing links and extracting information from web pages.
    """

    def __init__(self, url):
        """
        Initialize the Link object with a URL and parse its HTML content.
    
        Args:
            url (str): The URL of the web page.
        """
        self.url = url
        self.html = get_url(self.url)

    #This function is useless for the version of scrit it will be helpfull to mutli-classes img
    def selector(self, number):
        """
        Scrap images and return the class name of the specified image.
        
        Args:
            number (int): The index of the image to extract the class name from.
        
        Returns:
            str: The class name of the image, or "no class name" if not found.
        """
        try:
            pic_html = self.html.find_all('img')[number]['class']
            return pic_html
        except:
            pic_html = ["no class name"]
        return pic_html
    
    def c_list(self, n=30):
        """
        Create a list of unique class names from images on the page.
        
        Args:
            n (int): The number of images to consider.
        
        Returns:
            list: A list of unique class names.
        """
        names_list = []
        for i in range(n):
         if self.selector(i)[0] not in names_list:
             names_list.append(self.selector(i)[0])
        return names_list

    def get_picture(self, class_name, image_number = 0):
        """
        Get the URL of a picture with a specific class name.
        
        Args:
            class_name (str): The class name of the picture.
            image_number (int): The index of the image with the specified class name.
        
        Returns:
            str: The URL of the picture.
        """
        soup = self.html
        picture = soup.find_all('img', {'class': class_name})[image_number]['src']
        return picture
    
    def url_list(self, num, class_name="rg_i Q4LuWd"):
        """
        Return a list of picture URLs with a specific class name.
        
        Args:
            class_name (str): The class name of the pictures to retrieve.
        
        Returns:
            list: A list of URLs of pictures with the specified class name.
        """
        soup = self.html
        img_list = soup.find_all('img', {f'class': {class_name}})
        url_list = [img['src'] for img in img_list if 'src' in img.attrs]
        return url_list[0:num]

def load_path(dirname:str):
    """
    Create a directory for storing albums if it doesn't exist and return its path.

    Args:
        dirname (str): The name of the directory to be created.

    Returns:
        str: The path to the created directory.
    """
    path = os.path.join(os.getcwd(), 'static', 'images', 'album', dirname) 
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def download_image(url:str, dirname, file_name):
    """
    Download an image from a URL and save it to a specified directory with a given file name.

    Args:
        url (str): The URL of the image to download.
        dirname (str): The name of the directory to save the image in.
        file_name (str): The desired file name for the downloaded image.
    """
    if 'data:image/jpeg;base64' in url:
        data = url.split(',')[1]
        image_data = base64.b64decode(data)

    else : 
        image_data = requests.get(url).content
        
    # Open a file and write the decoded image data to it
    direction = load_path("_".join(dirname))
    with open(os.path.join(direction, f"{file_name}.jpg"), "wb+") as folder:
        folder.write(image_data) 
        
        
def download_page(url_list, dirname, file_name):
    """
    Download images from a list of URLs and save them with sequential file names.

    Args:
        url_list (list): A list of URLs of images to download.
        dirname (str): The name of the directory to save the images in.
        file_name (str): The base file name for the downloaded images.
    """
    for i, url in enumerate(url_list):
        download_image(url, dirname, f"{file_name}{i}")

def image_downloaded_count(num, entry):
    """
    Args:
        num (int): Total number of images to download.
        entry (str): name of directory file in static/images/album/

    Returns:
        str: percentage of images already downloaded.
    """
    return f"{len(os.listdir(f'static/images/album/{entry}'))/num * 100} %"


def create_tag(category, sample_size):
    """
    Create a tag image for a category with a specified sample size.

    Args:
        category (str): The category for which the tag image is created.
        sample_size (int): The sample size of the category.
    This function creates a tag image containing the category title and sample size information.
    """
    pic_icon = Image.open(f"static/images/album/{category}/{category}1.jpg")       
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
    
    album_tag = Image.open('static/images/blank_class.png')
    album_tag = album_tag.convert("RGBA")
    icon_pos=int((album_tag.size[1]-icon.size[1])/2)
    album_tag.paste(icon, (icon_pos, icon_pos), icon)
    
    pic = ImageDraw.Draw(album_tag)
    tag_title = category.capitalize()
    nb_pictures = f"{sample_size} pictures"
    font_size = 22
    font_color = (41, 41, 41)
    category_font = ImageFont.truetype('static/font/Georgia.ttf', 1.63*font_size)
    count_font = ImageFont.truetype('static/font/Georgia.ttf', font_size)
    pic.text((105,7), tag_title, font=category_font, fill=font_color)
    pic.text((113,52), nb_pictures, font=count_font, fill=font_color)
    album_tag.save(f"static/images/tags/{category}_tag.png", format="png")

def get_tags():
    """
    Get the file paths of tag images in the tags directory.

    Returns:
        list: A list of file paths to tag images.
    """
    image_directory = './static/images/tags'
    image_urls = [os.path.join(image_directory, filename) for filename in os.listdir(image_directory) if filename.endswith(('.png', '.jpg', '.jpeg'))]        
    return image_urls


def extract_train_classes(image_names):
    """
    A expliquer.

    Returns:
    """    
    pattern = r'\\([^\\]+)_tag'
    class1=image_names[0]
    class2=image_names[1]
    class_1 = re.search(pattern, class1)
    class_2 = re.search(pattern, class2)
    
    if class_1:
        # Extract the matched group, which is the content between the backslash and '_tag'
        class_1 = class_1.group(1)
        class_1 = class_1.capitalize()
    if class_2:
        # Extract the matched group, which is the content between the backslash and '_tag'
        class_2 = class_2.group(1)
        class_2 = class_2.capitalize()
    return (class_1, class_2)

def from_tag_get_name(tag_src):
    """
    Get the name of the category from its tag's src
    
    Args:
       A tag's path
        
    Returns:
       The name of the category associated with the tag
    """  
    pattern = r'.*[/\\](.*)_tag\.png'
    match = re.search(pattern, tag_src)
    match
    if match:
        category = match.group(1)
    return category

def from_name_get_album(category:str):
    """
    Create a list of all the images in a given album
    
    Args:
        Name of the category
        
    Returns:
        A list of path for all images in an album
    """  
    displayed_album =[]
    category = category.capitalize()
    list_display = os.listdir(f"./static/images/album/{category}")
    album_path = (f"./static/images/album/{category}/")
    for i in range(len(list_display)):
        print(i)
        displayed_album.append(os.path.join(album_path,list_display[i]))
    return displayed_album


