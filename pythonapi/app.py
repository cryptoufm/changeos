from flask import Flask, request
import json
import ipfsapi
import ipfsconnector as ipfs

app = Flask(__name__)


@app.route("/test/")
def testeo():
    return "bendi"

@app.route("/", methods=['POST'])
def eos():
    req = request.get_json()
    image = req.get('image', None)
    cui = req.get('cui', None)
    volID = req.get('vol', None)

    # Step 1
    # Hash the image into IPFS
    img_hash = ipfs.hashImage(image)['HASH']

    # Step 2
    # Call contract method Verify(VolunteerID ,CUI, imgHash) + Add


    return json.dumps(req)

@app.route("/reflist", methods=['GET'])
def reflist():

    # Call contract method voteList

    return 

@app.route("/voteInfo/<vote>", methods=['GET'])
def vote(vote):

    # Call contract method getVoteInfo

    return json.dumps(vote)

if __name__ == '__main__':
    api = ipfsapi.connect('127.0.0.1', 5001)
    app.run()





