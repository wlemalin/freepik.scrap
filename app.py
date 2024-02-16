# -*- coding: utf-8 -*-
"""
C'reated on Wed Feb  7 15:06:56 2024

"""

from flask import Flask, render_template, request, jsonify, session
from techprov2 import *  # Assuming this contains the necessary functionality like link(), research(), etc.
import os

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'  # Set a secure secret key

@app.route("/", methods=['GET', 'POST'])
def index():
    tag_list = get_tags()  # Assuming get_tags() is defined in techprov2 or elsewhere
    return render_template('search_form.html', tag_list=tag_list)

@app.route('/projet', methods=['GET', 'POST'])
def projet():
    if request.method == "POST":
        entry = request.form.get("url_entry").split(' ')
        img_link = link(research(*entry))  # Assuming link() and research() functions return necessary info
        num = int(request.form.get("num_entry"))
        image_url = img_link.num_list(num)  # Assuming num_list() returns a list of image URLs
        tag_list = get_tags()  # Refresh tag list, assuming it's needed for rendering
        
        if request.form.get('VAL') == "Search":
            session['image_url'] = image_url  # Store the list of image URLs in the session for persistence across requests
            # Render the page with the current list of image URLs
            return render_template("search_form.html", image_url=image_url, tag_list=tag_list, search=' '.join(entry), num=num)
        
        elif request.form.get('DOWN') == 'Download':
            # Use session-stored image URLs for downloading functionality
            download_page(session['image_url'], entry, "_".join(entry))  # Adjust download_page() as necessary
            create_tag("_".join(entry), len(os.listdir(f'album/{"_".join(entry)}')))
    # Default page rendering outside of POST condition
    tag_list = get_tags()
    return render_template('search_form.html', tag_list=tag_list)

@app.route('/remove-images', methods=['POST'])
def remove_images():
    # Ensure there's a list of images in the session
    if not session.get('image_url'):
        return jsonify({"success": False, "message": "No images to remove."})
    
    # Get the list of URLs to remove from the request's JSON body
    data = request.json
    urls_to_remove = set(data.get('urls', []))
    
    # Filter the session's list of images by removing the URLs to delete
    session['image_url'] = [url for url in session.get('image_url', []) if url not in urls_to_remove]
    
    # Confirm the removal via JSON response
    return jsonify({"success": session['image_url'], "message": "Images removed successfully."})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

