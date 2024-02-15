# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:06:56 2024

"""

from flask import Flask, render_template, request, jsonify
from techprov2 import *
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    tag_list = get_tags()
    return render_template('search_form.html', tag_list=tag_list)

@app.route('/projet', methods=['GET', 'POST'])
def projet():
    if request.method == "POST":
        entry = request.form.get("url_entry").split(' ')
        img_link = link(research(*entry))
        num = int(request.form.get("num_entry"))
        image_url = img_link.num_list(num)
        tag_list = get_tags()
        if request.form.get('VAL') == "Search":
            return render_template("search_form.html", 
                                   image_url=image_url,
                                   tag_list=tag_list,
                                   search = ' '.join(entry), 
                                   num=num)

        elif request.form.get('DOWN') == 'Download':    
            download_page(image_url, entry, "_".join(entry))
            create_tag("_".join(entry), num)
    tag_list = get_tags()
    return render_template('search_form.html', tag_list=tag_list)


if __name__ == '__main__':
    app.run(debug=True)



