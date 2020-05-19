from flask import Flask, json, request
from id_generator import create_id
from instrument import Instrument
from storage import instruments_db

app = Flask(__name__)

@app.route("/instruments")
def get_instruments():
    response = app.response_class(response=json.dumps(instruments_db), status=200, mimetype="application/json")
    return response

@app.route("/instruments/<instrument_id>")
def get_instrument_by_id(instrument_id):
    response = app.response_class(response=json.dumps(instruments_db[instrument_id]), status=200, mimetype="application/json")
    return response

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

@app.route("/instruments/reassign", methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)
