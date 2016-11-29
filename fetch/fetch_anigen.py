
import codecs
import pickle
import csv

fromyear = 2010

fin = codecs.open("./anigen/program.csv",encoding="utf-8")
dat=[]
reader = csv.reader(fin)
next(reader)
for row in reader:
	id = int(row[0])
	date = row[-1]
	clf = row[1]
	if("テレビアニメーション" in clf):
		dat.append([id,date])
fin.close()
dat.sort()
dy = [d for d in dat if (d[1]>=str(fromyear)+"-01-01")]
print(len(dy))

ids = [d[0] for d in dy]

fin = codecs.open("./anigen/anison.csv",encoding="utf-8")
reader = csv.reader(fin)
next(reader)
songs = []
for row in reader:
	if(len(row)!=8):
		print(row)
		break
		continue
	if(int(row[0]) in ids):
		songs.append([row[-2],row[-1]])
fin.close()
print(len(songs))


fout = open("./anigen/filtered.pkl","wb")
pickle.dump(songs,fout)
fout.close()

fout = codecs.open("./anigen/filtered.txt","w",encoding="utf-8")
fout.write(str(songs))
fout.close()
