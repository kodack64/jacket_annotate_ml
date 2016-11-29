
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
        title = metadata["album_title"]
        artist = metadata["album_artist_name"]
        filename = "./jpop/"+fid

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
    flist = glob.glob("./result/*.pkl")
    for fn in flist:
        year = fn.split("\\")[-1].replace("rec","").replace("hit","").replace(".pkl","")
        fin = open(fn,"rb")
        data = pickle.load(fin)
        fin.close()
        data.sort()
        done=0
        c=0
        for dat in data:
            artist = dat[2]
            album = dat[1]
            if(len(dat)==3):
                detail=''
            if(len(dat)==4):
                detail=dat[3]
            if(len(dat)>4):
                print(dat)
            if c>=done:
                fetchGraceNote(artist,album,detail,year+"_"+str(c))
                time.sleep(2)
            print("{2}:{0}-{1} fetched".format(artist,album,c))
            c+=1
