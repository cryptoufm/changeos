import ipfsapi


def hashImage(bytecode):
    res = api.add(bytecode)
    print(res)
    return res

def getImage(hash):
    img = api.cat(hash)
    print(type(img))
    return img


if __name__ == "__main__":
    api = ipfsapi.connect('127.0.0.1', 5001)

hs = hashImage(api,'dpi_0.png')
#getImage(api, 'QmdodXR3WWQGxmUmQsZy9PjuzYuUwAiEgCMif92ChLq2sJ')