from core import create_app
from flask import jsonify
config_name = 'dev'
app = create_app(config_name)

posts = [
    {
        "id": "12345678123456781234567812345678",
        "title": "Python is great",
        "body": "Python's convenience has made it the most popular language for machine learning and artificial intelligence. Python's flexibility has allowed Anyscale to make ML/AI scalable from laptops to clusters."
    },
    {
        "id": "d2841738-6f5b-4530-87d1-11349e27f29e",
        "title": "Flask is awsome",
        "body": "Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.[2] It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself. Extensions exist for object-relational mappers, form validation, upload handling, various open authentication technologies and several common framework related tools."
    },
    {
        "id": "216d8f22-4a66-434b-9efa-f6b5f1d4838d",
        "title": "Django is the best",
        "body": "Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source."
    }
]


@app.route("/")
def home():
    return "HomePage!"


@app.route("/posts")
def getPosts():
    return jsonify(posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
