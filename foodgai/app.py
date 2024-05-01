from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from pathlib import Path
import hashlib

import google.generativeai as genai
import os



app = Flask(__name__)

# Configure the API key
genai.configure(api_key="API_KEY")

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
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        activity = request.form["activity"]
        preferences = request.form["preferences"]
        intake = request.form["intake"]
        
        # Generate content
        content = f"You are AI health and diet expert. Your name is Dr. FoodGAI. The patient has come to you and ask for diet plan. Based on the below details respond starting to welcome him and introduce your self, addressing the patient in detail as a human and Provide diet plan: \n\n"
        content += f"Name: {name}\n"
        content += f"Age: {age}\n"
        content += f"Gender: {gender}\n"
        content += f"Level of physical activity: {activity}\n"
        content += f"Dietary Preferences: {preferences}\n"
        content += f"Current Dietary Intake: {intake}\n\n"
        content += f"The response should be in HTML code and bootstrap class for good styling."
        
        response = model.generate_content(content)
        generated_text = response.text
        
        # Format the generated text
        formatted_sections = format_generated_text(generated_text)

        return render_template("dietplan.html", formatted_sections=formatted_sections)
    return render_template("dietplan.html")


@app.route("/captureCook", methods=["GET", "POST"])
def captureCook():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        activity = request.form["activity"]
        preferences = request.form["preferences"]
        intake = request.form["intake"]
        
        # Generate content
        content = f"You are AI chef and diet expert. Your name is Chef. FoodGAI. The patient has uploaded the an image of the ingregients they have. You need to create a recipe based on the avaialble incredients in the imagee.and asked for diet plan. Based on the below details respond starting to welcome them and introduce yourself,  Provide the recipe and instrutions. \n\n"
        content += f"Dietary Preferences: {preferences}\n"
        content += f"The response should be in HTML code and bootstrap class for good styling."
        
        print(content)
        response = model.generate_content(content)
        generated_text = response.text
        
        # Format the generated text
        formatted_sections = format_generated_text(generated_text)

        return render_template("captureCook.html", formatted_sections=formatted_sections)
    return render_template("captureCook.html")


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

@app.route('/index2', methods=['GET', 'POST'])
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
        result = modelVision.generate_content(prompt_parts)   
        print(result.text)
        generated_text = result.text
            
        return render_template('index2.html', generated_text=generated_text)
    
    return render_template('index2.html')



if __name__ == "__main__":
    app.run(debug=True)
