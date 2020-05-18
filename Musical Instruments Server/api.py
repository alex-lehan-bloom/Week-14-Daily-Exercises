from flask import Flask, json, request
from id_generator import create_id
import storage

app = Flask(__name__)

@app.route("/instrument", methods=["POST"])
def add_instrument():
    content = request.form
    content = content.to_dict()
    instrument_id = create_id()
    storage.instruments[instrument_id] = content
    print(storage.instruments)
    response = {"instrumentId": instrument_id}
    return app.response_class(response=json.dumps(response), status=200, mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True)