from flask import Flask, request
import json
import ipfsapi
import ipfsconnector

app = Flask(__name__)


@app.route("/test/")
def testeo():
    return "bendi"

@app.route("/", methods=['POST'])
def eos():
    req = request.get_json()
    # image = req.get('image', None)
    # cui = req.get('cui', None)

    return json.dumps(req)

if __name__ == '__main__':
    api = ipfsapi.connect('127.0.0.1', 5001)
    app.run()





