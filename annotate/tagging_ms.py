import glob
import pickle
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64
import codecs
import time

fin = open("./../../key/ms.apikey")
key = fin.read().strip()
fin.close()

msheaders = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': key,
}
msparams = urllib.parse.urlencode({
    'visualFeatures': 'Categories,Tags,Faces,Description,ImageType,Color,Adult',
    'language': 'en',
})

def getFileList(base):
    searchPath = "./"+base+"/*/*.jpg"
    flist = glob.glob(searchPath)
    flist.sort()
    return flist

def MSTagging(fname,output):
    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    img = open(fname,"rb").read()
    conn.request("POST", "/vision/v1.0/analyze?%s" % msparams,img, msheaders)
    response = conn.getresponse()
    data = response.read()
    fout = codecs.open(output+"pkl","wb")
    pickle.dump(data,fout)
    fout.close()
    fout = codecs.open(output,"w",encoding="utf-8")
    fout.write(data.decode())
    fout.close()
#    print(data.decode())
    conn.close()
    print("{0} is fetched!",fname)

def MSTaggingAll(base):
    flist = getFileList(base)
    cnt=0
    allcnt = len(flist)
    for fn in flist:
        print(fn)
        msfile = fn.replace(".jpg",".mstag")
        if(not os.path.isfile(msfile)):
            MSTagging(fn,msfile)
            time.sleep(60.0/19)
        cnt+=1
        print("{0}/{1}".format(cnt,allcnt))

MSTaggingAll("anime")
MSTaggingAll("jpop")
