
import pickle
import glob

def fetchRec(fname):
	fin = open(fname)
	data = []
	dat = []
	rank=2
	for line in fin:
		line=line.strip().replace("\\","").replace("/","")
		try:
			r = int(line)
		except ValueError:
			r = 0
		if(r==rank):
			if(len(dat)<=3):
				dat.append("")
			if(len(dat)!=4):
				print(dat)
			data.append(dat)
			dat=[line]
			rank+=1
		else:
			dat.append(line)
	data.append(dat)
	print(len(data))
	fout =open(fname.replace("./raw","./result").replace(".txt",".pkl"),"wb")
	pickle.dump(data,fout)
	fout.close()

def fetchHit(fname):
	fin = open(fname)
	data=[]
	c=0
	r=1
	dat=[str(r)]
	for line in fin:
		line=line.strip().replace("\\","").replace("/","")
		dat.append(line)
		c+=1
		if((c%3==0) and (c!=0)):
			if(len(dat)!=4):
				print(dat)
			data.append(dat)
			r+=1
			dat=[str(r)]
	print(len(data))
	fout=open(fname.replace("./raw","./result").replace(".txt",".pkl"),"wb")
	pickle.dump(data,fout)
	fout.close()



def fetchAll():
	flist = glob.glob("./raw/hit*.txt")
	for fname in flist:
		print(fname)
		fetchHit(fname)

	flist = glob.glob("./raw/rec*.txt")
	for fname in flist:
		print(fname)
		fetchRec(fname)

fetchAll()
