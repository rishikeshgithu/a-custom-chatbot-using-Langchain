from flask import Flask, jsonify, request, render_template
from langchain_community.document_loaders import WebBaseLoader
import os
import re

# Set a user agent for web requests
os.environ['USER_AGENT'] = 'my-web-scraper/1.0'

# Step 1: Extract data from the URL using WebBaseLoader
loader = WebBaseLoader("https://brainlox.com/courses/category/technical")
documents = loader.load()

# Assuming the content is a long string with courses in a recognizable format
content = documents[0].page_content

# Example pattern to extract course titles and prices
courses = re.findall(r'LEARN (.*?)\n(.*?)\s+(\d+ Lessons)', content)

# Structure the data as a list of dictionaries
course_data = [{"title": title.strip(), "description": description.strip(), "lessons": lessons.strip()} for title, description, lessons in courses]

# Create a course mapping for easy access
course_mapping = {course["title"].lower(): course for course in course_data}

# Step 2: Create Flask RESTful API for returning the course data
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()

    # Check for specific course requests
    for title in course_mapping:
        if title in user_message:
            course_info = course_mapping[title]
            response = {
                "response": {
                    "title": course_info["title"],
                    "description": course_info["description"],
                    "lessons": course_info["lessons"]
                }
            }
            return jsonify(response)

    # If no course matches, provide a default response
    return jsonify({"response": "I'm not sure about that. Can you ask about a specific course?"})

if __name__ == '__main__':
    app.run(debug=True)
