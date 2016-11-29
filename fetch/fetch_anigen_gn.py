
import pygn
import pickle
import time
import traceback
import codecs
import glob
import sys

fin = open("./../../key/gn.apikey")
clientID = fin.readline().strip()
userID=fin.readline().strip()
fin.close()

def fetchGraceNote(qartist,qalbum,detail,fid):
    metadata = pygn.search(clientID=clientID, userID=userID, artist=qartist,album=qalbum)

    try:
        filename = "./anigen_gn/"+fid
        title = metadata["album_title"]
        artist = metadata["album_artist_name"]

        artist_origin = []
        for item in metadata["artist_origin"]:
            artist_origin.append(metadata["artist_origin"][item]["TEXT"])

        genre = []
        for item in metadata["genre"]:
            genre.append(metadata["genre"][item]["TEXT"])
        flag=False

        album_art_url = metadata["album_art_url"]

        print("url = " + album_art_url)
        if((len(album_art_url)>0) and ("Japan" in artist_origin)):
            f=open(filename+".gnpkl","wb")
            pickle.dump(metadata,f)
            f.close()
            fout = codecs.open(filename+".gnmeta","w",encoding="utf-8")
            fout.write("artist = {0}\n".format(artist))
            fout.write("title = {0}\n".format(title))
            fout.write("genre = {0}\n".format(genre))
            fout.write("img_gn = {0}\n".format(album_art_url))
            fout.write("origin = {0}\n".format(artist_origin))
            fout.write("query_title = {0}\n".format(qalbum))
            fout.write("query_artist = {0}\n".format(qartist))
            fout.close()
    except:
        print("********** {0} failed **********".format(filename))
        fout=codecs.open("_faillist.txt","a",encoding="utf-8")
        fout.write("*******************\n")
        fout.write(filename+"\n")
        fout.write(traceback.format_exc()+"\n")
        fout.close()

if __name__ == "__main__":
    fin = open("./anigen/filtered.pkl","rb")
    data =pickle.load(fin)
    fin.close()

    done=0
    c=0
    start=1200
    for dat in data:
        if(c<start):
            c+=1
            continue
        album = dat[0]
        artist = dat[1]
        fetchGraceNote(artist,album,"",str(c))
        time.sleep(1)
        print("{0} :fetched".format(c))
        c+=1
