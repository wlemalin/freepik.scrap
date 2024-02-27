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
        
        #if 'Download' button is clicked
        if request.form.get('DOWN') == 'Download':
            download_page(session['image_url'], entry, "_".join(entry)) # Use session-stored image URLs for downloading functionality
            create_tag("_".join(entry), len(os.listdir(f'static/images/album/{"_".join(entry)}')))
        #if 'Acceuil' button is clicked
        elif request.form.get('ACCUEIL') == "Accueil":
                tag_list = get_tags()
                return render_template("search_form.html",
                                tag_list = tag_list)
    tag_list = get_tags()
    return render_template('search_form.html', tag_list=tag_list)

@app.route('/projet', methods=['GET', 'POST'])
def projet():
    #if request method is post
    if request.method == "POST":
        
        #session to get 'url_entry' as global variable 
        session['entry'] = request.form.get("url_entry").split(' ')
        entry = session['entry']
        
        #create instence link for research on the web app (entry)
        img_link = link(generate_search_link(*entry))
        
        #get number of images (num_entry)
        num = int(request.form.get("num_entry"))
        
        #get data-src list of images on freepik
        image_url = img_link.num_list(num)
        
        #create tags 
        tag_list = get_tags()
        
        #if click on button 'Search' show images
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

@app.route('/start-training', methods=['POST'])
def start_training():
    data = request.json
    image_names = data.get('imageNames', [])
    # Here, you would start the training process with the provided image names
    
    # For demonstration, let's just print the names
    print("Starting training with images:", image_names)
    training_classes = extract_train_classes(image_names)
    session['training_classes'] = training_classes
    # Return a success response
    return jsonify({"success": session['training_classes'], "message": "Training started successfully with the provided images."})

@app.route('/album_viewer_tab', methods = ['POST'])
def album_viewer_tab():
    if request.form.get('ALBUM') == "Album":
        tag_list = get_tags()
        displayed_album = []
        return render_template("album_form.html",
                            tag_list = tag_list,
                            displayed_album = displayed_album)
  
       

@app.route('/album_dynamic_display', methods=['POST'])
def album_display():  
    data = request.json  # This is the JSON data sent from the client
    image_src = data.get('src', '')  # Extract the source of the clicked image
    displayed_album = from_name_get_album(from_tag_get_name(image_src))
    return jsonify({"imageUrls": displayed_album})
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

