from flask import Flask, Blueprint, render_template, request, jsonify, session, send_from_directory
from utils.folder_creation import check_init_folders
from scraping.google import  *
from cnn.model_building import *
import os

#get_tags, link, research, download_page, create_tag

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'  # Set a secure secret key

if __name__ == '__main__':
    check_init_folders()
    
entry = None
image_url = None
training_classes = None
accuracy = None

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        
        #if click on 'Download' button
        if request.form.get('DOWN') == 'Download':
            # Declare that we're using the global variable (user's entry declared thanks to jinja)
            global entry  
            global image_url 

            # Download pages and tags  
            download_page(image_url, entry, "_".join(entry)) # Use session-stored image URLs for downloading functionality
            create_tag("_".join(entry), len(os.listdir(f'static/images/album/{"_".join(entry)}')))
        
        #if click on 'Acceuil' button
        elif request.form.get('ACCUEIL') == "Accueil":
                tag_list = get_tags()
                return render_template("search_form.html",
                                tag_list = tag_list, image_url=image_url)    
    
    tag_list = get_tags()
    return render_template('search_form.html', tag_list=tag_list, image_url=image_url)


@app.route('/projet', methods=['GET', 'POST'])
def projet():
    #if request method is post
    if request.method == "POST":
        
        #if click on button 'Search' show images
        if request.form.get('VAL') == "Search":
            global entry
            entry = request.form.get("url_entry").split(' ')
            
            #get number of images (num_entry)
            num = int(request.form.get("num_entry"))

            #if url_entry is empty 
            if not request.form['url_entry'].strip():
                error = 'Le champ de recherche doit être rempli.'
                       
                #create tags 
                tag_list = get_tags()
                
                return render_template('search_form.html', tag_list=tag_list, error=error)
            
            else:
                print('la')
                #create instence link for research on the web app (entry)
                img_link = link(generate_search_link(*entry))
                
                #get data-src list of images on freepik
                global image_url
                image_url = img_link.url_list(num=num) 
                
                #create tags 
                tag_list = get_tags()
                
                return render_template("search_form.html", image_url=image_url, tag_list=tag_list, search=' '.join(entry), num=num)


        

@app.route('/models', methods = ['POST', 'GET'])
def training():
    if request.method == 'POST':
        if request.form.get('TRAIN') == "Models":
            tag_list = get_tags()
            return render_template("train_form.html",
                            tag_list = tag_list)

@app.route('/models_storage', methods = ['POST', 'GET'])
def my_models():
    if request.method == 'POST':
        if request.form.get('MODELS') == "My models":
            tag_list = get_tags()
            #fetch list of existing models
            models_list = []
            return render_template("train_form.html",
                            tag_list = tag_list,
                            models_list=models_list)

@app.route('/remove-images', methods=['POST'])
def remove_images():
    global entry  # Declare that we're using the global variable
    global image_url  # Declare that we're using the global variable
    data = request.json
    urls_to_remove = set(data.get('urls', []))
    image_url = [url for url in image_url if url not in urls_to_remove]
    # Confirm the removal via JSON response
    return jsonify({"success": image_url, "message": "Images removed successfully."})

@app.route('/start-training', methods=['POST'])
def start_training():
    global training_classes
    global accuracy
    data = request.json
    image_names = data.get('imageNames', [])
    training_classes = extract_train_classes(image_names)

    # Here, you would start the training process with the provided image names
    # For demonstration, let's just print the names
    print("Starting training with images:", image_names)
    accuracy = train_and_get_info(training_classes[0], training_classes[1])
    print(accuracy)
    return jsonify({"accuracy": accuracy})

@app.route('/train-result', methods=['POST'])
def result_training():
    if request.method == 'POST':
        if request.form.get('RESULT') == "Result":
            global accuracy    
            global training_classes
            tag_list=get_tags()
            return render_template("train_result.html",
                                   accuracy=accuracy,
                                   training_classes=training_classes,
                                   tag_list=tag_list)


@app.route('/model_dl', methods=['POST'])
def dl_model():
    if request.method == 'POST':
        if request.form.get('MOD-DL') == 'mod-dl':
            mod_name = f"Mod_{training_classes[0]}_{training_classes[1]}.keras"
            directory = os.path.join(os.getcwd(),"static","models")
            return send_from_directory(directory, mod_name, as_attachment=True)



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




