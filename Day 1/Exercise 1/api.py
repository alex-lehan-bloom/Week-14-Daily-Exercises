from flask import Flask
import json

import requests

app = Flask(__name__)

@app.route("/posts")
def get_posts():
    posts = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts_in_json = posts.json()
    response = app.response_class(response=json.dumps(posts_in_json), status=200, mimetype='application/json')
    return response

@app.route("/posts/<post_id>")
def get_post_by_id(post_id):
    post = requests.get("https://jsonplaceholder.typicode.com/posts/" + post_id)
    post_in_json = post.json()
    response = app.response_class(response=json.dumps(post_in_json), status=200, mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(debug=True)