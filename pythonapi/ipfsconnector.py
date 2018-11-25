from app import api

def hashImage(api, bytecode):
    res = api.add(bytecode)
    print(res)
    return res

def getImage(api, hash):
    img = api.cat(hash)
    print(type(img))
    return img