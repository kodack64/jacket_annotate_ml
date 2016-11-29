
import glob
import pickle
import codecs
import shutil

flist = glob.glob("./anigen_gn/*.gnmeta")
flist.sort()

hitlist = ["Game","Anime","TV","Animation"]

genres = set([])
c=0
ca=0
for ind,fn in enumerate(flist):
    fin = codecs.open(fn,"r",encoding="utf-8")
    animeFlag=False
    for line in fin:
        elem = line.split("=")
        if("genre" in elem[0]):
            gs = elem[1].strip().replace("[","").replace("]","").replace("\'","").replace(",","").split(" ")
            for g in gs:
                for h in hitlist:
                    if(h in g):
                        animeFlag=True
            if(animeFlag):
                for g in gs:
                    genres.add(g)
    if(animeFlag):
        ca+=1
    else:
        jpg = fn.replace(".gnmeta",".jpg")
        det = "./anigen_gn/susp/"+jpg.split("\\")[-1]
        shutil.move(jpg,det)
    c+=1
    fin.close()
print(c,ca)
