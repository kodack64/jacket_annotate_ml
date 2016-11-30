import glob
import pickle
import codecs
import i2v
import os
from PIL import Image

def getFileList(base):
    searchPath = "./"+base+"/*/*.jpg"
    flist = glob.glob(searchPath)
    flist.sort()
    return flist

print("load i2v")
clf = i2v.make_i2v_with_chainer("illust2vec_tag_ver200.caffemodel","tag_list.json")
print("load finish")

def I2vTagging(fname,output):
    img = Image.open(fname)
    data = clf.estimate_plausible_tags([img], threshold=0.0)
    fout = codecs.open(output+"pkl","wb")
    pickle.dump(data,fout)
    fout.close()
    fout = codecs.open(output,"w",encoding="utf-8")
    fout.write(str(data))
    fout.close()
#    print(data)

def I2vTaggingAll(base):
    flist = getFileList(base)
    cnt=0
    allcnt = len(flist)
    for fn in flist:
        print(fn)
        i2vfile = fn.replace(".jpg",".i2vtag")
        if(not os.path.isfile(i2vfile)):
            I2vTagging(fn,i2vfile)
        cnt+=1
        print("{0}/{1}".format(cnt,allcnt))


I2vTaggingAll("anime")
I2vTaggingAll("jpop")
I2vTagging("./test2.jpg","./test2.i2vresult")
