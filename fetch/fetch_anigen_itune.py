
import glob
import requests
import pickle
import codecs
import json
import time

fin = open("./anigen/filtered.pkl","rb")
dat =pickle.load(fin)
fin.close()

c=0
ct=0
start = 501
for d in dat:
    if c<start:
        c+=1
        continue
    try:
        url = "https://itunes.apple.com/search?"
        url += "term="+d[0]
        url += "&media=music&entity=album&country=JP&limit=10&lang=ja_jp&genreId=29"
        res = requests.get(url)
        time.sleep(1.0)
        js = json.loads(res.text)
        rc = js["resultCount"]
        if(rc==0):
            rstr = "nores"
        else:
            rstr = "noanime"
        for ind in range(rc):
            results = []
            title = js["results"][ind]["collectionName"]
            artist = js["results"][ind]["artistName"]
            genre = js["results"][ind]["primaryGenreName"]
            img_itune = js["results"][ind]["artworkUrl100"]
            if(genre=="アニメ"):
                fout = open("./anigen_anime/{0}.pkl".format(c),"wb")
                pickle.dump([title,artist,genre,img_itune],fout)
                fout.close()
                fout = codecs.open("./anigen_anime/{0}.meta".format(c),"w",encoding="utf-8")
                fout.write("title={0}\n".format(title))
                fout.write("artist={0}\n".format(artist))
                fout.write("genre={0}\n".format(genre))
                fout.write("img_itune={0}\n".format(img_itune))
                fout.close()
                ct+=1
                rstr="ok"
                break
        c+=1
        print(c,ct,rstr)
    except:
        pass
