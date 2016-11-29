
import glob
import pickle
from urllib import request

def downloadImageFromInternet(source, output):
    response = request.urlopen(source)
    if response.code != 200:
        return -1
    with open(output, "wb") as fout:
        fout.write(response.read())

flist = glob.glob("./jpop/*.gnmeta")
for fn in flist:
    fin = open(fn,"r")
    for line in fin:
        elem = line.split("=")
        if("img_gn" in elem[0]):
            url = (elem[1]+"="+elem[2]).strip()
            print(url)
            downloadImageFromInternet(url,fn.replace(".gnmeta",".jpg"))
