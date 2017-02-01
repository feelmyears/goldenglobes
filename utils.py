import pickle

def save(dObj, sFilename):
    """Given an object and a file name, write the object to the file using pickle."""

    f = open(sFilename, "w")
    p = pickle.Pickler(f)
    p.dump(dObj)
    f.close()


def load(sFilename):
    """Given a file name, load and return the object stored in the file."""

    f = open(sFilename, "r")
    u = pickle.Unpickler(f)
    dObj = u.load()
    f.close()
    return dObj