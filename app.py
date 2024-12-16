# from flask import Flask, render_template, request
# import google.generativeai as genai  # LLM provider
# import markdown  # For rendering Markdown content
# import os

# # Initialize Flask app
# app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'  # For flashing messages

# # Access API key (confidential)
# with open("C:/Users/kesan/OneDrive/Desktop/innometics/key.txt", "r") as file:
#     key = file.read().strip()

# genai.configure(api_key=key)

# # Instruction to the model
# sys_prompt = """You are an expert, helpful and sensible AI Code Reviewer. 
# User will give you the code written by them. 
# You should analyze the code and identify all the bugs or errors. 
# You will most probably receive any of the following 3 cases of inputs - incorrect code, correct code or irrelevant out of scope request.
# In case 1, that is, if you receive an incorrect code, organize your response into 3 sections; 'Bug Report', 'Corrected Code' and 'Suggestions'. 
# In the 'Bug Report' section, mention the name of the error, the corresponding erroneous part in the given code and a brief description about the error. 
# By the name of error, I mean the standard names like 'key error', 'Name error', 'Type error' etc. 
# Errors can be even spelling errors. If you receive just one line or only a few lines of code, you should point out mistakes in it although it may not be complete. 
# The section title 'Bug Report' should be in boldface and in red color.
# In the 'Corrected Code' section, provide the corrected code with proper comments within the code.
# The section title 'Corrected Code' should be in boldface and in green color.
# In the 'Suggestions' section, provide user-friendly feedback that helps them to improve their code, code writing style etc. Keep the 3rd section brief. 
# The section title 'Suggestions' should be in boldface and in Blue color. 
# The section titles shall have a comparatively higher font size, say 28.
# Sometimes, the user might have already defined a variable which may be anything including a dataframe. But user may give you some line in between as the input. Skillfully identify such things and communicate with the user and provide a sensible output. 
# In case 2, that is, if there are no mistakes or bugs, just describe the code and mention general suggestions. In this case, no need to organise content into 3 sections as said above.
# In case 3, that is, the user provides a code in any other language other than Python or some irrelevant content out of scope, politely decline their request."""

# # Initialize Gemini model
# model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", 
#                               system_instruction=sys_prompt)

# # Route for home page
# @app.route("/", methods=["GET", "POST"])
# def index():
#     response_html = ""  # Store the formatted AI response
#     if request.method == "POST":
#         if "code_text" in request.form:
#             user_code = request.form.get("code_text")
#             # Generate AI response
#             response = model.generate_content(user_code)
#             # Convert Markdown to HTML with syntax highlighting
#             response_html = markdown.markdown(response.text, extensions=["fenced_code", "codehilite"])

#         elif "code_file" in request.files:
#             uploaded_file = request.files["code_file"]
#             if uploaded_file.filename != "":
#                 file_contents = uploaded_file.read().decode("utf-8")
#                 response = model.generate_content(file_contents)
#                 response_html = markdown.markdown(response.text, extensions=["fenced_code", "codehilite"])

#     return render_template("index.html", response=response_html)

# # Run Flask app
# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request
import google.generativeai as genai  # LLM provider
import markdown  # For rendering Markdown content
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For flashing messages

# Access API key (confidential)
with open("key.txt", "r") as file:
    key = file.read().strip()

genai.configure(api_key=key)

# Instruction to the model
sys_prompt = """
You are an expert, helpful, and sensible AI Code Reviewer. 
The user will give you code in any programming language.
Analyze the code and identify all bugs, errors, and inefficiencies. 
Organize your response into:
1. **Bug Report**: Include error names, erroneous parts, and descriptions (Red, 28px font).
2. **Corrected Code**: Provide corrected code with comments (Green, 28px font).
3. **Suggestions**: Brief feedback for improvement (Blue, 28px font).
If the language is unsupported or content is irrelevant, politely decline the request.
"""


# Initialize Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", 
                              system_instruction=sys_prompt)


# Route for home page
@app.route("/", methods=["GET", "POST"])
def index():
    response_html = ""
    if request.method == "POST":
        lang = request.form.get("language")  # Get language input from user
        user_code = request.form.get("code_text", "")
        if "code_file" in request.files:
            uploaded_file = request.files["code_file"]
            if uploaded_file.filename:
                file_contents = uploaded_file.read().decode("utf-8")
                user_code = file_contents
                lang = os.path.splitext(uploaded_file.filename)[-1][1:]  # Infer language from extension

        if user_code:
            # Combine user's code with language context
            prompt = f"Language: {lang.capitalize()}\n\n{user_code}"
            response = model.generate_content(prompt)  # No instruction parameter
            response_html = markdown.markdown(response.text, extensions=["fenced_code", "codehilite"])
        else:
            response_html = "No code provided."

    return render_template("index.html", response=response_html)


# @app.route("/", methods=["GET", "POST"])
# def index():
#     response_html = ""  # Store the formatted AI response
#     if request.method == "POST":
#         if "code_text" in request.form:
#             user_code = request.form.get("code_text")
#             # Generate AI response
#             response = model.generate_content(user_code)
#             # Convert Markdown to HTML with syntax highlighting
#             response_html = markdown.markdown(response.text, extensions=["fenced_code", "codehilite"])

#         elif "code_file" in request.files:
#             uploaded_file = request.files["code_file"]
#             if uploaded_file.filename != "":
#                 file_contents = uploaded_file.read().decode("utf-8")
#                 response = model.generate_content(file_contents)
#                 response_html = markdown.markdown(response.text, extensions=["fenced_code", "codehilite"])

#     return render_template("index.html", response=response_html)

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
