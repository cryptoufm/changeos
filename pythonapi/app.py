from flask import Flask, request, Response
import json
import ipfsconnector
from eosfactory.eosf import *

app = Flask(__name__)


@app.route("/test/")
def testeo():
    print("IS PRINTING")    
    return "test is  success"

@app.route("/", methods=['POST'])
def eos():
    req = request.get_json()
    image = req.get('image_hash', None)
    cui = req.get('citizenuid', None)
    volunteer_id = req.get('volunteer_id', None)

    # Step 1
    # Hash the image into IPFS
    img_hash = ipfsconnector.hashImage(image)

    # Step 2
    # Call contract method Verify(VolunteerID ,CUI, imgHash) + Add
    contract.push_action("insert", {
        "citizen_uid": cui, 
        "volunteer_id": volunteer_id, 
        "image_hash": img_hash['Hash']
        }, 
        permission=host)

    resp = Response(json.dumps(req), status=200, mimetype='application/json')

    return resp

@app.route("/referendum", methods=['GET'])
def reflist():

    # Call contract method voteList
    votes = host.table("petition", host)
    js = json.dumps(votes.json)
    resp = Response(js, status=200, mimetype='application/json')
    
    return resp

@app.route("/voteInfo/<uid>", methods=['GET'])
def vote(uid):

    # Call contract method getVoteInfo
    votes = host.table("petition", host)
    for vote in votes.json["Rows"]:   
    	if (vote["citizenuid"] == uid):
		value = vote
    if (value): 
    	resp = Response(json.dumps(value), status=200, mimetype='application/json')
    	return resp
    else:
	return "Invalid UID"

contract = ContractBuilder("referendum")
contract.build()
#print("INIT TESTNET")
reset()
create_master_account("master")
create_account("host", master)
contract = Contract(host, contract.path())
contract.deploy()


if __name__ == '__main__':
    app.run(host='0.0.0.0')




