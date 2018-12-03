from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import json
app = Flask(__name__)
CORS(app)
with open("db4.json", "r") as f:
    db = json.load(f)

@app.route('/highlights/<vod_id>')
@cross_origin()

def hello(vod_id):
    print(db)
    return jsonify(db.get(vod_id, {}))

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')