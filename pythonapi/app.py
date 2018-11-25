from flask import Flask, request
import json
import ipfsconnector

app = Flask(__name__)


@app.route("/test/")
def testeo():
    return "test success"

@app.route("/", methods=['POST'])
def eos():
    req = request.get_json()
    image = req.get('image_hash', None)
    cui = req.get('citizenuid', None)
    volID = req.get('volunteer_id', None)

    # Step 1
    # Hash the image into IPFS
    img_hash = ipfsconnector.hashImage(image)

    # Step 2
    # Call contract method Verify(VolunteerID ,CUI, imgHash) + Add


    return img_hash['Name']

@app.route("/reflist", methods=['GET'])
def reflist():

    # Call contract method voteList

    return 

@app.route("/voteInfo/<vote>", methods=['GET'])
def vote(vote):

    # Call contract method getVoteInfo

    return json.dumps(vote)

if __name__ == '__main__':
    app.run()





