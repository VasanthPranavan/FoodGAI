from flask import Flask, request, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key
genai.configure(api_key="your_api_key_here")

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


if __name__ == "__main__":
    app.run(debug=True)
