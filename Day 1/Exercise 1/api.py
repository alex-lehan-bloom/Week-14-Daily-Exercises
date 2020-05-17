from flask import Flask
import json
import ast
from JsonablePost import JsonablePost
import GlobalVariables

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
    post = requests.get("https://jsonplaceholder.typicode.com/posts/{}".format(post_id))
    post_in_json = post.json()
    response = app.response_class(response=json.dumps(post_in_json), status=200, mimetype='application/json')
    return response


@app.route("/posts/<post_id>/comments")
def get_comments_of_specific_post(post_id):
    comments = requests.get("https://jsonplaceholder.typicode.com/posts/{}/comments".format(post_id))
    comments_in_json = comments.json()
    response = app.response_class(response=json.dumps(comments_in_json), status=200, mimetype='application/json')
    return response


@app.before_first_request
def add_date_to_posts():
    posts = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts_in_json = posts.json()
    for post in posts_in_json:
        new_jsonable_instance = JsonablePost(post)
        post_with_date = new_jsonable_instance.create_json()
        post_with_date = ast.literal_eval(post_with_date)
        GlobalVariables.posts_with_dates[post.get('id')] = post_with_date
    print(GlobalVariables.posts_with_dates)

if __name__ == '__main__':
    app.run(debug=True)
