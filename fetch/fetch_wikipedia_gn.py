
import pygn
import pickle
import time
import traceback
import glob


fin = open("./../../key/gn.apikey")
clientID = fin.readline().strip()
userID=fin.readline().strip()
fin.close()

def fetchGraceNote(qartist,qalbum,detail,fid):
    metadata = pygn.search(clientID=clientID, userID=userID, artist=qartist,album=qalbum)

    try:
        filename = "./wiki_gn/"+fid
        title = metadata["album_title"]
        artist = metadata["album_artist_name"]

        genre = []
        for item in metadata["genre"]:
            genre.append(metadata["genre"][item]["TEXT"])
        album_art_url = metadata["album_art_url"]

        print("url = " + album_art_url)
        if(len(album_art_url)>0):
            f=open(filename+".gnpkl","wb")
            pickle.dump(metadata,f)
            f.close()
            fout = open(filename+".gnmeta","w")
            fout.write("artist = {0}\n".format(artist))
            fout.write("title = {0}\n".format(title))
            fout.write("genre = {0}\n".format(genre))
            fout.write("img_gn = {0}\n".format(album_art_url))
            fout.close()
    except:
        print("********** {0} failed **********".format(filename))
        fout=open("_faillist.txt","a")
        fout.write("*******************\n")
        fout.write(filename+"\n")
        fout.write(traceback.format_exc()+"\n")
        fout.close()

if __name__ == "__main__":
    fin = open("./wiki/wiki.pkl","rb")
    data = pickle.load(fin)
    fin.close()
    done=0
    for ind,dat in enumerate(data):
        album = dat[0]
        artist = dat[1]
        if ind>=done:
            fetchGraceNote(artist,album,"",str(ind))
            time.sleep(2)
            print("{2}:{0}-{1} fetched".format(artist,album,ind))
        else:
            print("{2}:{0}-{1} passed".format(artist,album,ind))
