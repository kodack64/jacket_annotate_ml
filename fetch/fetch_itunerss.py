
import requests
import pickle
import codecs
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import io, sys
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.setrecursionlimit(10000)

url = "https://itunes.apple.com/jp/rss/topalbums/limit=200/"

gen = "anime"
#gen = "jpop"

genreIdAnime = 29
genreIdJpop = 27
if gen in "anime":
    url = url+"genre={0}/xml".format(genreIdAnime)
if gen in "jpop":
    url = url+"genre={0}/xml".format(genreIdJpop)

res = requests.get(url)

xml = BeautifulSoup(res.text,"lxml")
titles = []
artist = []
imurl = []
genre = []
for e in xml.find_all("im:name"):
    titles.append(e.string.replace("/","").replace("\\","").replace("<","").replace(">","").replace("?","").replace("!","").replace("\"","").replace("*","").replace(":",""))
for e in xml.find_all("im:artist"):
    ast = e.string
    if(len(ast)>100):
        ast = e.string[0:100]
    artist.append(ast.replace("/","").replace("\\","").replace("<","").replace(">","").replace("?","").replace("!","").replace("\"","").replace("*","").replace(":",""))
for e in xml.find_all("im:image"):
    if(e.get("height")=="170"):
        imurl.append(e.string)
for e in xml.find_all("category"):
    genre.append(e.get("term"))
res = list(zip(titles,artist,genre,imurl))
res = [[str(d[0]),str(d[1]),str(d[2]),str(d[3])] for d in res]

fout = codecs.open("itune.txt","w",encoding="utf-8")
for item in res:
    fout.write(str(item)+"\n")
fout.close()

for ind in range(len(res)):
    fout = codecs.open("./itune_"+gen+"/"+str(ind)+".meta","w",encoding="utf-8")
    fout.write("artist = {0}\n".format(res[ind][1]))
    fout.write("title = {0}\n".format(res[ind][0]))
    fout.write("genre = {0}\n".format([res[ind][2]]))
    fout.write("img = {0}\n".format(res[ind][3]))
    fout.close()
    fout = codecs.open("./itune_"+gen+"/"+str(ind)+".pkl","wb")
    pickle.dump(res[ind],fout)
    fout.close()
