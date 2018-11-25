from app import api

def hashImage(bytecode):
    res = api.add(bytecode)
    print(res)
    return res

def getImage(hash):
    img = api.cat(hash)
    print(type(img))
    return img