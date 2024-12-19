def load_env():
    f = open(".env", "r").read().split("\n")
    res = {}
    for elt in f:
        res[elt.split("=")[0]] = elt.split("=")[1]
    
    return res