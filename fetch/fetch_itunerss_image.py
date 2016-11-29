from urllib import request
import glob
import pickle

def downloadImageFromInternet(source, output):
    response = request.urlopen(source)
    if response.code != 200:
        return -1
    with open(output, "wb") as fout:
        fout.write(response.read())

flist = glob.glob("./itune_anime/*.pkl")
for fn in flist:
    fin = open(fn,"rb")
    dat = pickle.load(fin)
    fin.close()
    dat[3] = dat[3].replace("170x170","650x650")
    res = downloadImageFromInternet(dat[3],fn.replace(".pkl",".jpg"))
    if(res == -1):
        print(fn)
