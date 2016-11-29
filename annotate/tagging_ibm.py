import requests
import glob
import pickle
import os
import codecs
import time
import base64
import json
from watson_developer_cloud import VisualRecognitionV3

fin = open("./../../key/ibm.apikey")
key = fin.read().strip()
fin.close()

def getFileList(base):
    searchPath = "./"+base+"/*/*.jpg"
    flist = glob.glob(searchPath)
    flist.sort()
    return flist

def IbmTagging(fname,output):
    img = open(fname, 'rb').read()
    str_encode_file = base64.b64encode(img).decode("utf-8")
    vr = VisualRecognitionV3("2016-05-20",api_key=key)
    with open(fname, 'rb') as image_file:
    	data = vr.classify(images_file=image_file)
    fout = codecs.open(output+"pkl","wb")
    pickle.dump(data,fout)
    fout.close()
    fout = codecs.open(output,"w",encoding="utf-8")
    fout.write(str(data))
    fout.close()
    print(data)
    print("{0} is fetched!",fname)

def IbmTaggingAll(base):
    flist = getFileList(base)
    cnt=0
    allcnt = len(flist)
    for fn in flist:
        print(fn)
        ibmfile = fn.replace(".jpg",".ibmtag")
        if(not os.path.isfile(ibmfile)):
            IbmTagging(fn,ibmfile)
#            time.sleep(60.0/19)
        else:
            print("passed")
        cnt+=1
        print("{0}/{1}".format(cnt,allcnt))

IbmTaggingAll("anime")
IbmTaggingAll("jpop")
