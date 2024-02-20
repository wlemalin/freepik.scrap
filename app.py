from flask import Flask, Blueprint, render_template, request, jsonify, session
from utils.folder_creation import check_init_folders
from scraping.techprov2 import  *
import os
#get_tags, link, research, download_page, create_tag

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'  # Set a secure secret key

if __name__ == '__main__':
    # Initial checks
    check_init_folders()

@app.route("/", methods=['GET', 'POST'])
def index():
    entry = session.get('entry')
    if request.method == "POST":
        if request.form.get('DOWN') == 'Download':
            download_page(session['image_url'], entry, "_".join(entry)) # Use session-stored image URLs for downloading functionality
            create_tag("_".join(entry), len(os.listdir(f'album/{"_".join(entry)}')))
        elif request.form.get('ACCUEIL') == "Accueil":
                tag_list = get_tags()
                return render_template("search_form.html",
                                tag_list = tag_list)
    tag_list = get_tags()
    return render_template('search_form.html', tag_list=tag_list)

@app.route('/projet', methods=['GET', 'POST'])
def projet():
    if request.method == "POST":
        session['entry'] = request.form.get("url_entry").split(' ')
        entry = session['entry']
        img_link = link(generate_search_link(*entry))
        num = int(request.form.get("num_entry"))
        image_url = img_link.num_list(num)
        tag_list = get_tags()
        if request.form.get('VAL') == "Search":
            session['image_url'] = image_url  # Store the list of image URLs in the session for persistence across requests
            return render_template("search_form.html", image_url=image_url, tag_list=tag_list, search=' '.join(entry), num=num)
    return render_template('search_form.html', tag_list=tag_list)

@app.route('/models', methods = ['POST', 'GET'])
def training():
    if request.method == 'POST':
        if request.form.get('TRAIN') == "Training":
            tag_list = get_tags()
            return render_template("train_form.html",
                            tag_list = tag_list)

@app.route('/remove-images', methods=['POST'])
def remove_images():
    if not session.get('image_url'): # Ensure there's a list of images in the session
        return jsonify({"success": False, "message": "No images to remove."})
    data = request.json
    urls_to_remove = set(data.get('urls', []))
    session['image_url'] = [url for url in session.get('image_url', []) if url not in urls_to_remove]
    # Confirm the removal via JSON response
    return jsonify({"success": session['image_url'], "message": "Images removed successfully."})

if __name__ == '__main__':
    app.run(debug=True)

