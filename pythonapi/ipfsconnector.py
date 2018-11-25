import io
import ipfsapi
import base64

def hashImage(b64):
    bytecode = base64.b64decode(b64)

    img = io.BytesIO(bytecode)    
    res = api.add(img)
    print(res)
    return res

def getImage(hash):
    img = api.cat(hash)
    print(type(img))
    return img

def initipfs():
    return ipfsapi.connect('127.0.0.1', 5001)

api = initipfs()
