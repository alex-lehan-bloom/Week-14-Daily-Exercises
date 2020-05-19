from flask import Flask, json, request, send_file, render_template
from id_generator import create_id
from instrument import Instrument
from storage import instruments_db, users_db
from validators import validator
from werkzeug.utils import secure_filename
from registration_form import RegistrationForm
import time
import re
import io
import os.path


app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user_id = create_id()
        users_db[create_id()] = form.username.data
        return render_template("home.html")
    return render_template('registration.html', form=form)

@app.route("/instruments")
def get_instruments():
    response = app.response_class(response=json.dumps(instruments_db), status=200, mimetype="application/json")
    return response

@app.route("/instruments/<instrument_id>")
def get_instrument_by_id(instrument_id):
    response = app.response_class(response=json.dumps(instruments_db[instrument_id]), status=200, mimetype="application/json")
    return response

@app.route("/instruments/find/<search_query>")
def search_for_instrument(search_query):
    search_results = {}
    start_time = time.perf_counter()
    for instrument_id in instruments_db:
        instrument = instruments_db[instrument_id]['instrument']
        match = re.search(search_query.lower(),instrument.lower())
        if match:
            search_results[instrument_id] = instruments_db[instrument_id]
    end_time = time.perf_counter()
    if search_results == {}:
        search_results["results"] = "No instruments match your search term."
    search_results["searchTimeInMS"] = end_time - start_time
    response = app.response_class(response=json.dumps(search_results), status=200, mimetype="application/json")
    return response

@app.route('/instruments/download_image/<image_name>')
def download_instrument_images(image_name):
    print(os.path.join('images', "test"))
    try:
        with open(os.path.join('images', image_name), "rb") as bites:
            return send_file(
                io.BytesIO(bites.read()),
                attachment_filename=image_name,
                mimetype='image/jpg'
            )
    except EnvironmentError:
        response_body = {"error": "File not found."}
        return app.response_class(response=json.dumps(response_body), status=404, mimetype="application/json")

@app.route("/instruments/user/<user_name>")
def get_instrument_by_user(user_name):
    users = {}
    for instrument in instruments_db:
        if user_name.lower() == instruments_db.get(instrument).get('user').lower():
            users[instrument] = instruments_db.get(instrument)
    response = app.response_class(response=json.dumps(users), status=200, mimetype="application/json")
    return response

@app.route("/instruments", methods=["POST"])
def add_instrument():
    content = request.form
    new_instrument = Instrument(content)
    instrument_id = create_id()
    instruments_db[instrument_id] = new_instrument
    response = {"instrumentId": instrument_id}
    return app.response_class(response=json.dumps(response), status=200, mimetype='application/json')

@app.route("/instruments/assign", methods=['POST'])
def reassign_instrument():
    content = request.form
    content = content.to_dict()
    response_body = {}
    for instrument in instruments_db:
        if content["instrumentId"] == instrument:
            instruments_db[instrument]["user"] = content["user"]
            response_body[instrument] = instruments_db[instrument]
    response = app.response_class(response=json.dumps(response_body), status=200, mimetype="application/json")
    return response

@app.route("/instruments/add_video/<instrument_id>", methods=['POST'])
def add_video_to_instrument(instrument_id):
    content = request.form
    content = content.to_dict()
    instruments_db[instrument_id]["video"] = content["video"]
    response_body = {instrument_id: instruments_db[instrument_id]}
    response = app.response_class(response=json.dumps(response_body), status=200, mimetype="application/json")
    return response

@app.route("/instruments/add_image/<instrument_id>", methods=['POST'])
def add_image(instrument_id):
    if not validator.instrument_exists(instrument_id):
        response_body = {"status": "Instrument with ID '{}' does not exist.".format(instrument_id)}
    else:
        images = request.files.getlist('image[]')
        if len(images) > 2:
            response_body = {"status": "Upload failed. You can only upload two images at a time."}
        else:
            response_body = {"status": "Upload successful.", "images":[]}
            for image in images:
                filename = secure_filename(image.filename)
                image.save('images/' + filename)
                instruments_db[instrument_id]['images'].append(filename)
                response_body['images'].append(filename)
    response = app.response_class(response=json.dumps(response_body), status=200, mimetype="application/json")
    return response

@app.route("/instruments/user/<username>", methods=['DELETE'])
def delete_instruments_for_user(username):
    response_body = {}
    for instrument_id in list(instruments_db.keys()):
        if instruments_db[instrument_id]['user'].lower() == username.lower():
            response_body[instrument_id] = instruments_db[instrument_id]
            del instruments_db[instrument_id]
    if response_body == {}:
        response_body = {"Status": "No instruments were assigned to {}.".format(username)}
    response = app.response_class(response=json.dumps(response_body), status=200, mimetype="application/json" )
    return response


if __name__ == '__main__':
    app.run(debug=True)
