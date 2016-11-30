import requests
import glob
import pickle
import os
import codecs
import time
import base64
import json

fin = open("./../../key/google.apikey")
key = fin.read().strip()
fin.close()

def getFileList(base):
    searchPath = "./"+base+"/*/*.jpg"
    flist = glob.glob(searchPath)
    flist.sort()
    return flist

def GoTagging(fname,output):
    img = open(fname, 'rb').read()
    str_encode_file = base64.b64encode(img).decode("utf-8")
    str_json_data = {
        'requests': [{
            'image': {'content': str_encode_file},
            'features': [{
                'type': "LABEL_DETECTION",
                'maxResults': 100
            }]
        }]
    }
    jsd = json.dumps(str_json_data)
    response = requests.post(url='https://vision.googleapis.com/v1/images:annotate?key='+key,
        data=jsd,
        headers={'Content-Type': 'application/json'})
    data = response.text
    fout = codecs.open(output+"pkl","wb")
    pickle.dump(data,fout)
    fout.close()
    fout = codecs.open(output,"w",encoding="utf-8")
    fout.write(data)
    fout.close()
#    print(data)
    print("{0} is fetched!",fname)

def GoTaggingAll(base):
    flist = getFileList(base)
    cnt=0
    allcnt = len(flist)
    for fn in flist:
        print(fn)
        gofile = fn.replace(".jpg",".gotag")
        if(not os.path.isfile(gofile)):
            GoTagging(fn,gofile)
#            time.sleep(60.0/19)
        else:
            print("passed")
        cnt+=1
        print("{0}/{1}".format(cnt,allcnt))

GoTaggingAll("anime")
GoTaggingAll("jpop")
GoTagging("./test2.jpg","./test2.goresult")
