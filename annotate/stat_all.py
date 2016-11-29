
import glob
import pickle
import json

def loadMS(imgpath):
    pklpath = imgpath.replace(".jpg",".mstagpkl")
    fin = open(pklpath,"rb")
    dat = pickle.load(fin)
    fin.close()
    dat = json.loads(dat.decode())
#    print(dat)
    tags = dat["description"]["tags"]
    caption = dat["description"]["captions"][0]["text"]
    adultScore = dat["adult"]["adultScore"]
    racyScore = dat["adult"]["racyScore"]
    try:
        categories = dat["categories"]
    except:
        categories = {"name":"","score":0.0}
    color = dat["color"]
    rtn = {}
    rtn["mstags"]=tags
    rtn["caption"]=caption
    rtn["msrate"]={"adult":adultScore,"racy":racyScore}
    rtn["categories"]=categories
    rtn["color"]=color
    return rtn

def loadGo(imgpath):
    pklpath = imgpath.replace(".jpg",".gotagpkl")
    fin = open(pklpath,"rb")
    dat = pickle.load(fin)
    fin.close()
    dat = json.loads(dat)
    try:
        tags = [des["description"] for des in dat["responses"][0]["labelAnnotations"]]
    except:
        tags = []
    rtn = {"gotags":tags}
    return rtn

def loadI2v(imgpath):
    pklpath = imgpath.replace(".jpg",".i2vtagpkl")
    fin = open(pklpath,"rb")
    dat = pickle.load(fin)[0]
    fin.close()
    rate = list(dat["rating"])
    tag = []
    for item in dat["general"]:
        if(item[1]>0.1):
            tag.append(item)
    rtn = {"i2vtags":tag,"i2vrate":rate}
    return rtn

def loadAllTag(imgpath):
    dat_ms = loadMS(imgpath)
    dat_go = loadGo(imgpath)
    dat_i2v = loadI2v(imgpath)
    dat = dict(list(dat_ms.items())+list(dat_go.items())+list(dat_i2v.items())+list({"imgpath":imgpath}.items()))
    return dat

def load(base):
    flist = glob.glob("./{0}/*/*.jpg".format(base))
    dat = []
    for ind,fn in enumerate(flist):
        print("{0}/{1}".format(ind,len(flist)))
        dat.append(loadAllTag(fn))
    fout = open(base+".pkl","wb")
    pickle.dump(dat,fout)
    fout.close()

load("anime")
load("jpop")
