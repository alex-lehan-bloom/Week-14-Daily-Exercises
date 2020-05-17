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
    generate_posts_with_created_date()
    generate_comments_for_each_post()
    print(GlobalVariables.posts_with_dates)


def generate_posts_with_created_date():
    posts = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts_in_json = posts.json()
    for post in posts_in_json:
        new_jsonable_instance = JsonablePost(post)
        post_with_date = new_jsonable_instance.create_json()
        post_with_date = ast.literal_eval(post_with_date)
        GlobalVariables.posts_with_dates[post.get('id')] = post_with_date


def generate_comments_for_each_post():
    comments = requests.get("https://jsonplaceholder.typicode.com/comments")
    comments_in_json = comments.json()
    id = 1
    comments_for_a_specific_post = []
    for comment in comments_in_json:
        if int(comment.get('postId')) == id:
            comments_for_a_specific_post.append(comment)
        else:
            GlobalVariables.posts_with_dates[id]['comments'] = comments_for_a_specific_post
            comments_for_a_specific_post = [comment]
            id += 1



if __name__ == '__main__':
    app.run(debug=True)
