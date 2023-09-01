from joppy.api import Api
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

joplin_token = os.getenv("JOPLIN_TOKEN")


api = Api(token=joplin_token)

def get_api():
    return api

def get_notebook(name):
    notebooks = api.get_all_notebooks()

    for notebook in notebooks:
        if name in notebook.title:
            return notebook.id
    
    return "NO SUCH NOTEBOOKS!"
    

def get_note(name):
    notebooks = api.get_all_notes()

    for notebook in notebooks:
        if name in notebook.title:
            return notebook.id
    
    
    return "NO SUCH NOTES!"
