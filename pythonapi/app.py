from flask import Flask, request, Response
import json
import ipfsconnector
from eosfactory.eosf import *
import argparse, sys, time

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE])

CONTRACT_WORKSPACE = "/home/eegodinez/changeos-contracts/contracts/referendum"

INITIAL_RAM_KBYTES = 8
INITIAL_STAKE_NET = 3
INITIAL_STAKE_CPU = 3

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
    value = {}
    for vote in votes.json["rows"]:   
        if (vote["citizen_uid"] == uid):
            value = vote
    if (value): 
        resp = Response(json.dumps(value), status=200, mimetype='application/json')
        return resp
    else:
        return "Invalid UID"


def stats():
    print_stats(
        [master, host, alice, carol],
        [
            "core_liquid_balance",
            "ram_usage",
            "ram_quota",
            "total_resources.ram_bytes",
            "self_delegated_bandwidth.net_weight",
            "self_delegated_bandwidth.cpu_weight",
            "total_resources.net_weight",
            "total_resources.cpu_weight",
            "net_limit.available",
            "net_limit.max",
            "net_limit.used",
            "cpu_limit.available",
            "cpu_limit.max",
            "cpu_limit.used"
        ]
    )



def setUpClass(cls):
    SCENARIO('''
    There is the ``master`` account that sponsors the ``host``
    account equipped with an instance of the ``tic_tac_toe`` smart contract. There
    are two players ``alice`` and ``carol``. We are testing that the moves of
    the game are correctly stored in the blockchain database.
    ''')

    testnet.verify_production()
            
    create_master_account("master", testnet)
    create_account("host", master,
        buy_ram_kbytes=INITIAL_RAM_KBYTES, stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
        
    if not testnet.is_local():
        cls.stats()

    contract = Contract(host, CONTRACT_WORKSPACE)
    contract.build(force=False)

    try:
        contract.deploy(payer=master)
    except errors.ContractRunningError:
        pass


def setUp(self):
    pass

def tearDown(self):
    pass


def tearDownClass(cls):
    if testnet.is_local():
        stop()
    else:
        cls.stats()


testnet = None


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''
    This is a unit test for the ``tic-tac-toe`` smart contract.
    It works both on a local testnet and remote testnet.
    The default option is local testnet.
    ''')

    parser.add_argument(
        "alias", nargs="?",
        help="Testnet alias")

    parser.add_argument(
        "-t", "--testnet", nargs=4,
        help="<url> <name> <owner key> <active key>")

    parser.add_argument(
        "-r", "--reset", action="store_true",
        help="Reset testnet cache")

    args = parser.parse_args()

    testnet = get_testnet(args.alias, args.testnet, reset=args.reset)
    testnet.configure()

    if args.reset and not testnet.is_local():
        testnet.clear_cache()
    

    app.run(host='0.0.0.0')




