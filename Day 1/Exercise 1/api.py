from flask import Flask
import json

import requests

app = Flask(__name__)

@app.route("/posts")
def get_posts():
    posts = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts_to_json = posts.json()
    response = app.response_class(response=json.dumps(posts_to_json), status=200, mimetype='application/json')
    return response

if __name__ == '__main__':
    app.run(debug=True)