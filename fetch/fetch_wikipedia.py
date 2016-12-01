
import glob
import codecs
import pickle

flist = glob.glob("./wiki/*.txt")
fout = codecs.open("./wiki/wiki.txt","w",encoding="utf-8")
songs = []
for fn in flist:
    fin = codecs.open(fn,encoding="utf-8")
    for line in fin:
        elem = line.split("（")
        if(len(elem)<=1):
            continue
        sn = elem[0].strip()
        elem = elem[1].split("；")
        if(len(elem)<=1):
            continue
        ar = elem[0].strip()
        songs.append([sn,ar])
        fout.write("{0} *** {1}\n".format(sn,ar))
    fin.close()
fout.close()
fout = open("./wiki/wiki.pkl","wb")
pickle.dump(songs,fout)
fout.close()
