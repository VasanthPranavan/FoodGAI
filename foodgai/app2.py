from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pathlib import Path
import hashlib
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure the API key
genai.configure(api_key="")

# Set up the generative model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

uploaded_files = []

def upload_if_needed(pathname: str) -> list[str]:
    path = Path(pathname)
    hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
    try:
        existing_file = genai.get_file(name=hash_id)
        return [existing_file.uri]
    except:
        pass
    uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
    return [uploaded_files[-1].uri]

# Define allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        




        image_path = Path("image.jpeg")
        image_part = {
            "mime_type": "image/jpeg",
            "data": image_path. read_bytes()
        }

        prompt_parts = [
            "You are AI chef and diet expert. Your name is Chef. FoodGAI. The patient has uploaded the an image of the ingregients they have. You need to create a recipe based on the avaialble incredients in the imae.and asked for diet plan. Based on the below details respond starting to welcome them and introduce yourself,  Provide the recipe and instrutions.\n\n Name: Sruthi \nDietary Preferences: vegetarian:\n",
            image_part
        ]    

       # print(prompt_parts.text)

        # Generate content
        result = model.generate_content(prompt_parts)   
        print(result.text)
        generated_text = result.text
            
        return render_template('index2.html', generated_text=generated_text)
    
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)
