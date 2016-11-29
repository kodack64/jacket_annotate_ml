
import glob
import pickle
from urllib import request
import time
import codecs
import os

def downloadImageFromInternet(source, output):
    response = request.urlopen(source)
    if response.code != 200:
        print("!!!!! {0} returned".format(response.code))
        return -1
    with open(output, "wb") as fout:
        fout.write(response.read())

flist = glob.glob("./anigen_gn/*.gnmeta")
flist.sort()
for ind,fn in enumerate(flist):
    fin = codecs.open(fn,"r",encoding="utf-8")
    for line in fin:
        elem = line.split("=")
        if("img_gn" in elem[0]):
            url = (elem[1]+"="+elem[2]).strip()
            print(ind,url)
            fetchimg = fn.replace(".gnmeta",".jpg")
            if(not os.path.isfile(fetchimg)):
                print(fetchimg)
                downloadImageFromInternet(url,fetchimg)
                time.sleep(0.3)
            else:
                print("{0} exists".format(fetchimg))
