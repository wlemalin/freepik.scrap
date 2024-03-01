from os import mkdir, path

def check_init_folders() -> None:
    folders = [
        './static/images/tags', 
        './static/images/album',
        './static/models'
    ]
    for folder in folders:
        if not path.exists(folder):
            try:
                mkdir(folder)
            except Exception as e:
                print(f"Error while creating needed folders {e}")
                exit(1)