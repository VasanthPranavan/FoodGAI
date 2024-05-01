from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from pathlib import Path
import hashlib

import google.generativeai as genai
import os

app = Flask(__name__)

# Configure the API key
genai.configure(api_key="YOUR_API_KEY")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def format_generated_text(generated_text):
    generated_text = generated_text.replace("```html", "").replace("```", "")
    sections = generated_text
    return sections


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/dietplan", methods=["GET", "POST"])
def dietplan():
    if request.method == "POST":
        # Handle form submission
        # Your code for generating diet plan goes here
        return render_template("dietplan.html")
    return render_template("dietplan.html")


generation_config_Vision = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings_Vision = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

modelVision = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config_Vision,
    safety_settings=safety_settings_Vision,
)

@app.route("/captureCook", methods=["GET", "POST"])
def captureCook():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'image' not in request.files:
            return render_template('captureCook.html', error="No image uploaded")
        
        image = request.files['image']
        
        # Check if the file is empty
        if image.filename == '':
            return render_template('captureCook.html', error="No image selected")
        
        # Save the file to a temporary location
        filename = secure_filename(image.filename)
        image_path = Path("uploads") / filename
        image.save(image_path)
        
        # Get form data
        name = request.form.get('name')
        dietary_preferences = request.form.get('dietaryPreferences')
        
        # Generate content
        prompt_parts = [
            f"You are AI chef and diet expert. Your name is Chef. FoodGAI. The patient has uploaded an image of the ingredients they have. You need to create a recipe based on the available ingredients in the image and asked for diet plan. Based on the below details respond starting to welcome them and introduce yourself,  Provide the recipe and instructions.\n\n Name: {name} \nDietary Preferences: {dietary_preferences}\n The response should be in HTML code and bootstrap class for good styling. Use nice colors for fonts ",
            {"mime_type": "image/jpeg", "data": image_path.read_bytes()}
        ]
        
        result = modelVision.generate_content(prompt_parts)   
        generated_text = result.text
        
        # Format the generated text
        formatted_sections = format_generated_text(generated_text)    
        return render_template('captureCook.html', formatted_sections=formatted_sections)
    
    return render_template('captureCook.html')


if __name__ == "__main__":
    app.run(debug=True)
