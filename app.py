# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:06:56 2024

"""

from flask import Flask, render_template, request
from techprov2 import *
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    image_directory = 'static/images/tags'
    image_urls = [os.path.join(image_directory, filename) for filename in os.listdir(image_directory) if filename.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('search_form.html', image_urls=image_urls)

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('search_form.html', image_urls=image_urls)

@app.route('/projet', methods=['GET', 'POST'])
def projet():
    if request.method == "POST":
        entry = request.form.get("url_entry").split(' ')
        img_link = link(research(*entry))
        num = int(request.form.get("num_entry"))
        image_url = img_link.num_list(num)
        image_directory = 'static/images/tags'
        image_urls = [os.path.join(image_directory, filename) for filename in os.listdir(image_directory) if filename.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if request.form.get('VAL') == "Search":
            return render_template("search_form.html", 
                                   image_url=image_url,
                                   image_urls=image_urls,
                                   search = ' '.join(entry), 
                                   num=num)

        elif request.form.get('DOWN') == 'Download':    
            download_page(image_url, entry, "_".join(entry))
            create_tag("_".join(entry), num)
    image_directory = 'static/images/tags'
    image_urls = [os.path.join(image_directory, filename) for filename in os.listdir(image_directory) if filename.endswith(('.png', '.jpg', '.jpeg', '.gif'))]        
    return render_template('search_form.html', image_urls=image_urls)




if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)



