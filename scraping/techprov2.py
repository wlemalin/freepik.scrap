from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import random
import os
import re


def get_url(url):
    '''
    Function to retrieve the HTML content of a given URL by using a fake user agent.
    
    Args:
        url (str): The URL to retrieve the content from.
        
    Returns:
        str: The HTML content of the URL.
    '''
    user_agents_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        ]
    r = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
    return r.text


def generate_search_link(*words):
    '''
    Function to generate a search link for the Freepik website based on provided keywords.
    
    Args:
        *words (str): Variable number of keyword arguments representing the search terms.
        
    Returns:
        str: A URL link for the search results on the Freepik website.
    '''
    return "https://fr.freepik.com/search?ai=exclude&format=search&page=1&query=" + f'{"%20".join(words)}&type=photo'

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
        self.html = BeautifulSoup(get_url(self.url), 'html.parser')

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
    
    def c_list(self, n):
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
        picture = soup.find_all('img', {'class': class_name})[image_number]['data-src']
        return picture
    
    def url_list(self, class_name="lzy"):
        """
        Return a list of picture URLs with a specific class name.
        
        Args:
            class_name (str): The class name of the pictures to retrieve.
        
        Returns:
            list: A list of URLs of pictures with the specified class name.
        """
        soup = self.html
        img_list = soup.find_all('img', {f'class': {class_name}})
        url_list = [img['data-src'] for img in img_list if 'data-src' in img.attrs]
        return url_list
     
    def page_selection(self, page=1):
        """
        Select a specific page on fr.freepik.com.
        
        Args:
            page (int): The page number to select.
        
        Returns:
            Link: A new Link object representing the selected page.
        """
        p_url = re.sub(r'page=[^&]+', f'page={page}', self.url)
        return link(p_url)
    
    def page_list(self, num:int):
        """
        Generate a list of URLs for a specified number of pages.
        
        Args:
            num (int): The number of page URLs to generate.
        
        Returns:
            list: A list of URLs for the specified number of pages.
        """
        p_list = [self.page_selection(page=i+1).url for i in range(num)]
        return p_list
    
    def num_list(self, num=60):
        """
        Generate a list of picture URLs from multiple pages.
        
        Args:
            num (int): The total number of picture URLs to retrieve.
        
        Returns:
            list: A list of picture URLs up to the specified number.
        """
        page = self.url_list()
        p=1
        
        while len(page) < num:
                p+=1
                page += self.page_selection(p).url_list()
        
        return page[0:num]

def load_path(dirname:str):
    """
    Create a directory for storing albums if it doesn't exist and return its path.

    Args:
        dirname (str): The name of the directory to be created.

    Returns:
        str: The path to the created directory.
    """
    path = os.path.join(f'{os.getcwd()}\\static\\images', 'album/', dirname) 
    if not os.path.exists(path):
        os. makedirs(path)
    return path



def download_image(url, dirname, file_name):
    """
    Download an image from a URL and save it to a specified directory with a given file name.

    Args:
        url (str): The URL of the image to download.
        dirname (str): The name of the directory to save the image in.
        file_name (str): The desired file name for the downloaded image.
    """
    direction = load_path("_".join(dirname))
    with open(os.path.join(direction, f"{file_name}.jpg"), "wb+") as folder:
        folder.write(requests.get(url).content) 

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
    pattern = r'\\([^\\]+)_tag'
    class1=image_names[0]
    class2=image_names[1]
    class_1 = re.search(pattern, class1)
    class_2 = re.search(pattern, class2)
    if class_1:
        # Extract the matched group, which is the content between the backslash and '_tag'
        class_1 = class_1.group(1)
        print(class_1)
    if class_2:
        # Extract the matched group, which is the content between the backslash and '_tag'
        class_2 = class_2.group(1)
        print(class_2)
    return (class_1, class_2)
        
load_path("chat")