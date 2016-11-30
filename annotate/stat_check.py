
import pickle
import matplotlib.pyplot as plt
import random
from gensim import corpora
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
import numpy as np

fin = open("anime.pkl","rb")
anime = pickle.load(fin)
fin.close()

fin = open("jpop.pkl","rb")
jpop = pickle.load(fin)
fin.close()
#print(anime[0])
def getColorSet():
    colorset = set([])
    for item in anime:
        for c in item["color"]["dominantColors"]:
            colorset.add(c)
    for item in jpop:
        for c in item["color"]["dominantColors"]:
            colorset.add(c)
    return colorset

def getDominantColorRatio(c):
    ca = 0
    cj = 0
    for item in anime:
         if (c in item["color"]["dominantColors"]):
             ca+=1
    for item in jpop:
         if (c in item["color"]["dominantColors"]):
             cj+=1
    return (ca/len(anime),cj/len(jpop))

def checkColor():
    label = []
    ratanime = []
    ratjpop = []
    for c in getColorSet():
        rat = getDominantColorRatio(c)
        print(c,rat)
        label.append(c)
        ratanime.append(rat[0])
        ratjpop.append(rat[1])
    left = np.array(list(range(len(label))))
    plt.bar(left-0.2,ratanime,width=0.4,tick_label=label,align="center",color="red",label="anime")
    plt.bar(left+0.2,ratjpop,width=0.4,tick_label=label,align="center",color="blue",label="jpop")
    plt.ylabel("ratio")
    plt.legend(loc=0)
    plt.savefig("mscolor.png")
    plt.show()
#checkColor()

###################################################################################################

def checkRate():
    pxa = []
    pya = []
    pza = []
    paa = []
    pba = []
    random.shuffle(anime)
    random.shuffle(jpop)
    for item in anime:
        pxa.append(item["i2vrate"][0][1])
        pya.append(item["i2vrate"][1][1])
        pza.append(item["i2vrate"][2][1])
        paa.append(item["msrate"]["adult"])
        pba.append(item["msrate"]["racy"])
    pxj = []
    pyj = []
    pzj = []
    paj = []
    pbj = []
    for item in jpop:
        pxj.append(item["i2vrate"][0][1])
        pyj.append(item["i2vrate"][1][1])
        pzj.append(item["i2vrate"][2][1])
        paj.append(item["msrate"]["adult"])
        pbj.append(item["msrate"]["racy"])
    plt.subplot(3,1,1)
    plt.xlabel("safety")
    plt.ylabel("ratio")
    plt.hist(pxa,normed=True,bins=50,alpha=0.3,range=(0,1),label="jpop",color="red")
    plt.hist(pxj,normed=True,bins=50,alpha=0.3,range=(0,1),label="anime",color="blue")
    plt.subplot(3,1,2)
    plt.xlabel("questionnaire")
    plt.hist(pya,normed=True,bins=50,alpha=0.3,range=(0,1),label="jpop",color="red")
    plt.hist(pyj,normed=True,bins=50,alpha=0.3,range=(0,1),label="anime",color="blue")
    plt.subplot(3,1,3)
    plt.xlabel("explicit")
    plt.hist(pza,normed=True,bins=50,alpha=0.3,range=(0,1),label="jpop",color="red")
    plt.hist(pzj,normed=True,bins=50,alpha=0.3,range=(0,1),label="anime",color="blue")
    plt.legend()
    plt.savefig("i2vrate.png")
    plt.show()

    plt.subplot(2,1,1)
    plt.xlabel("adult")
    plt.ylabel("ratio")
    plt.hist(paa,normed=True,bins=50,alpha=0.3,range=(0,1),label="jpop",color="red")
    plt.hist(paj,normed=True,bins=50,alpha=0.3,range=(0,1),label="anime",color="blue")
    plt.subplot(2,1,2)
    plt.xlabel("racy")
    plt.hist(pba,normed=True,bins=50,alpha=0.3,range=(0,1),label="jpop",color="red")
    plt.hist(pbj,normed=True,bins=50,alpha=0.3,range=(0,1),label="anime",color="blue")
    plt.legend()
    plt.savefig("msrate.png")
    plt.show()
#checkRate()

###################################################################################################

def getCategorySet():
    catset = set([])
    for item in anime:
        for c in item["categories"]:
            try:
                catset.add(c[0])
            except:
                pass
    for item in jpop:
        for c in item["categories"]:
            try:
                catset.add(c[0])
            except:
                pass
    return catset

def getCategoryRatio():
    catl = getCategorySet()
    rats = []
    for cat in catl:
        ca = 0
        cj = 0
        for item in anime:
            for c in item["categories"]:
                try:
                    if(cat in c[0]):
                        ca+=1
                except:
                    pass
        for item in jpop:
            for c in item["categories"]:
                try:
                    if(cat in c[0]):
                        cj+=1
                except:
                    pass
        if ((ca!=0) and (cj!=0)):
            rats.append([float(ca/len(anime)/cj*len(jpop)),str(cat)])
    rats.sort()
    for it in rats:
        print(it)
#getCategoryRatio()


###################################################################################################

from gensim import models
def makeCorpus():
    import io, sys
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    corp_anime = []
    corp_jpop = []

    tagset = set([])
    tag = "gotags"
    for item in anime:
        if(len(item[tag])>0):
            pack = []
            for st in item[tag]:
                st = st[0].replace(" ","")
                tagset.add(st)
                pack.append(st)
            corp_anime.append(" ".join(pack))
    for item in jpop:
        if(len(item[tag])>0):
            pack = []
            for st in item[tag]:
                st = st[0].replace(" ","")
                tagset.add(st)
                pack.append(st)
            corp_jpop.append(" ".join(pack))
    trf = TfidfVectorizer(max_df=0.9,min_df=5)
    trf.fit(corp_anime+corp_jpop)
    xa = trf.transform(corp_anime).toarray()
    xj = trf.transform(corp_jpop).toarray()
    xjtr,xjte = train_test_split(xj,test_size=0.2)
    xatr,xate = train_test_split(xa,train_size=xjtr.shape[0],test_size=xjte.shape[0])
    voc = trf.vocabulary_
#    print(len(voc))
#    print(voc)

    xtr = np.vstack((xatr,xjtr))
#    print(xtr.shape,xatr.shape,xjtr.shape)
    xte = np.vstack((xate,xjte))
#    print(xte.shape,xate.shape,xjte.shape)

    ytr = [0]*xatr.shape[0]+[1]*xjtr.shape[0]
    yte = [0]*xate.shape[0]+[1]*xjte.shape[0]

    from sklearn.ensemble import RandomForestClassifier
    from sklearn import svm
    import xgboost as xgb
    from sklearn.grid_search import GridSearchCV


    param = {"n_estimators" : list(range(25,35,1)), "max_depth":[2]}
    rf = RandomForestClassifier()

    '''
    param = {
        "learning_rate" : np.linspace(0.1,0.2,1),
        "n_estimators" : np.arange(500,600,300),
        "min_child_weight" : np.arange(1,2,2),
        "max_depth" : np.arange(3,4,12),
        "gamma" : np.linspace(0.1,0.2,1),
        "subsample" : np.linspace(0.8,0.9,1),
        "colsample_bytree" : np.linspace(0.8,0.9,1)
    }
    print(param)
    rf = xgb.XGBClassifier()
    '''

    grd = GridSearchCV(rf,param)
    grd.fit(xtr,ytr)
    clf = grd.best_estimator_

    imp = clf.feature_importances_
    imps = []
    for ind,inv in enumerate(imp):
        imps.append([inv,ind])
    imps.sort()
    imps.reverse()
    fout = open("importance.txt","w")
    for item in imps:
        key = [key for key, value in voc.items() if value == item[1]][0]
        fout.write("{0} {1}\n".format(key,item[0]))
    fout.close()

    train_sc = clf.score(xtr,ytr)
    test_sc = clf.score(xte,yte)
    print(train_sc,test_sc)
    print(grd.best_params_)
#makeCorpus()


def linearSep():
    import io, sys
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    corp_anime = []
    corp_jpop = []

    print(anime[0])
    tagset = set([])
    tag = "i2vtags"
    for item in anime:
        if(len(item[tag])>0):
            pack = []
            for st in item[tag]:
                st = st[0].replace(" ","")
                tagset.add(st)
                pack.append(st)
            corp_anime.append(" ".join(pack))
    for item in jpop:
        if(len(item[tag])>0):
            pack = []
            for st in item[tag]:
                st = st[0].replace(" ","")
                tagset.add(st)
                pack.append(st)
            corp_jpop.append(" ".join(pack))
    trf = TfidfVectorizer(max_df=1.0,min_df=10)
    trf.fit(corp_anime+corp_jpop)
    xa = trf.transform(corp_anime).toarray()
    xj = trf.transform(corp_jpop).toarray()
    xjtr,xjte = train_test_split(xj,test_size=0.2)
    xatr,xate = train_test_split(xa,train_size=xjtr.shape[0],test_size=xjte.shape[0])
    voc = trf.vocabulary_

    xtr = np.vstack((xatr,xjtr))
    xte = np.vstack((xate,xjte))
    ytr = [0]*xatr.shape[0]+[1]*xjtr.shape[0]
    yte = [0]*xate.shape[0]+[1]*xjte.shape[0]

    from sklearn import svm
    from sklearn.feature_selection import RFE,RFECV
    param = {"C" : [0.01,0.1,1,10,100,1000]}
    rf = svm.LinearSVC()
    rfe = RFE(estimator=rf,n_features_to_select=10000,step=10)
    rfe.fit(xtr,ytr)
    xtrt = rfe.transform(xtr)
    xtet = rfe.transform(xte)
    rf.fit(xtrt,ytr)
    print(rf.score(xtrt,ytr))
    print(rf.score(xtet,yte))

    supIndex = rfe.transform(list(range(len(xtr[0]))))[0]
    def getIdKey(id):
        return [key for key, value in voc.items() if value == id][0]
    feats = [[rf.coef_[0][i],getIdKey(v)] for i,v in enumerate(supIndex)]
    feats.sort()
    print("\n".join(list(map(str,feats[0:5]))))
    feats.reverse()
    print("\n".join(list(map(str,feats[0:5]))))

#    feats = [[abs(rf.coef_[0][i]),rf.coef_[0][i],v,getIdKey(v)] for i,v in enumerate(supIndex)]
#    feats.sort()
#    print("\n".join(list(map(str,feats))[::-1]))
#linearSep()

def expl():
    import io, sys
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    tagset = set([])
    tags = ["i2vtags","mstags","gotags"]
    for tag in tags:
        for item in anime:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                tagset.add(t)
        for item in jpop:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                tagset.add(t)
    idtag=list(tagset)
    idtag.sort()
    idtag = ["anime/jpop"]+idtag
    tagid = {}
    for id,tag in enumerate(idtag):
        tagid[tag]=id
    feature = np.zeros((len(anime)+len(jpop),len(idtag)))
    cnt = 0
    for item in anime:
        for tag in tags:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                feature[cnt][tagid[t]]=st[1]
        feature[cnt][0]=0
        cnt+=1
    for item in jpop:
        for tag in tags:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                feature[cnt][tagid[t]]=st[1]
        feature[cnt][0]=1
        cnt+=1
    from sklearn.decomposition import PCA
    pca = PCA()
    pca.fit(feature)
    mat = pca.get_covariance()
    covs = list(zip(mat[0][1:],idtag[1:]))
    covs.sort()
    cors = []
    for ind in range(len(mat[0])):
        cors.append([mat[0][ind]/np.sqrt(mat[ind][ind]*mat[0][0]),idtag[ind]])
    cors.sort()
    import codecs
    fout = codecs.open("cov.txt","w",encoding="utf-8")
    for item in covs:
        fout.write("{0} {1}\n".format(item[0],item[1]))
    fout.close()
    fout = codecs.open("cor.txt","w",encoding="utf-8")
    for item in cors:
        fout.write("{0} {1}\n".format(item[0],item[1]))
    fout.close()

    corsgo = [d for d in cors if "gotags_" in d[1]]
    corsms = [d for d in cors if "mstags_" in d[1]]
    corsi2v = [d for d in cors if "i2vtags_" in d[1]]
    fout = codecs.open("cor_go.txt","w",encoding="utf-8")
    for item in corsgo:
        fout.write("{0} {1}\n".format(item[0],item[1]))
    fout.close()
    fout = codecs.open("cor_ms.txt","w",encoding="utf-8")
    for item in corsms:
        fout.write("{0} {1}\n".format(item[0],item[1]))
    fout.close()
    fout = codecs.open("cor_i2v.txt","w",encoding="utf-8")
    for item in corsi2v:
        fout.write("{0} {1}\n".format(item[0],item[1]))
    fout.close()

    print(covs[:10])
    print(covs[::-1][:10])
#expl()

def corplot():
    fin = open("cor.txt")
    go = []
    i2v = []
    ms = []
    for line in fin:
        elem = line.split(" ")
        if("gotags_" in elem[1]):
            go.append(float(elem[0]))
        elif("i2vtags_" in elem[1]):
            i2v.append(float(elem[0]))
        elif("mstags_" in elem[1]):
            ms.append(float(elem[0]))
        else:
            print("unknown tag {0}".format(elem[1]))
    plt.subplot(3,1,1)
    st = -0.25
    en = 0.25
    bins=100
    plt.ylabel("ratio")
    plt.ylim([0,15])
    plt.hist(go,normed=True,bins=bins,alpha=1.0,range=(st,en),color="red",label="google")
    plt.legend()
    plt.subplot(3,1,2)
    plt.ylim([0,15])
    plt.ylabel("ratio")
    plt.hist(ms,normed=True,bins=bins,alpha=1.0,range=(st,en),color="red",label="microsoft")
    plt.legend()
    plt.subplot(3,1,3)
    plt.ylim([0,15])
    plt.ylabel("ratio")
    plt.hist(i2v,normed=True,bins=bins,alpha=1.0,range=(st,en),color="red",label="Illustration2Vec")
    plt.legend()
    plt.savefig("corhist.png")
    plt.show()
    fin.close()
#corplot()

def precision():
    import io, sys
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    tagset = set([])
    tags = ["i2vtags","mstags","gotags"]
    for tag in tags:
        for item in anime[:len(jpop)]:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                tagset.add(t)
        for item in jpop:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                tagset.add(t)
    idtag=list(tagset)
    idtag.sort()
    idtag = ["anime/jpop"]+idtag
    tagid = {}
    for id,tag in enumerate(idtag):
        tagid[tag]=id
    feature = np.zeros((len(jpop)*2,len(idtag)))
    cnt = 0
    for item in anime[:len(jpop)]:
        for tag in tags:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                feature[cnt][tagid[t]]=st[1]
        feature[cnt][0]=1
        cnt+=1
    for item in jpop:
        for tag in tags:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                feature[cnt][tagid[t]]=st[1]
        feature[cnt][0]=0
        cnt+=1

    percAnime = [0.0]*(len(feature[0])-1)
    percJpop = [0.0]*(len(feature[0])-1)
    percSum = [0.0]*(len(feature[0])-1)
    for itemId in range(len(feature)):
        percSum += feature[itemId][1:]
        if(feature[itemId][0]==1):
            percAnime+=feature[itemId][1:]
        else:
            percJpop+=feature[itemId][1:]

    feature[feature>0]=1
    cntAnime = [0]*(len(feature[0])-1)
    cntJpop = [0]*(len(feature[0])-1)
    cntSum = [0]*(len(feature[0])-1)
    for itemId in range(len(feature)):
        cntSum += feature[itemId][1:]
        if(feature[itemId][0]==1):
            cntAnime+=feature[itemId][1:]
        else:
            cntJpop+=feature[itemId][1:]
    percAnime = percAnime/percSum
    percJpop = percJpop/percSum
    cntAnime = cntAnime/cntSum
    cntJpop = cntJpop/cntSum
    cntItem = len(feature)
    thr = 10
    info = [[cntSum[ind],percSum[ind],idtag[ind+1],cntAnime[ind],cntJpop[ind],percAnime[ind],percJpop[ind]] for ind in range(len(percAnime)) if cntSum[ind]>=thr]
    info.sort()
    import codecs
    fout = codecs.open("precision.txt","w",encoding="utf-8")
    for item in info:
        fout.write(str(item)+"\n")
    fout.close()

    info_go = [d for d in info if "gotags_" in d[2]]
    info_ms = [d for d in info if "mstags_" in d[2]]
    info_i2v = [d for d in info if "i2vtags_" in d[2]]
    fout = codecs.open("precision_go.txt","w",encoding="utf-8")
    for item in info_go:
        fout.write(str(item)+"\n")
    fout.close()
    fout = codecs.open("precision_ms.txt","w",encoding="utf-8")
    for item in info_ms:
        fout.write(str(item)+"\n")
    fout.close()
    fout = codecs.open("precision_i2v.txt","w",encoding="utf-8")
    for item in info_i2v:
        fout.write(str(item)+"\n")
    fout.close()

    info_go.sort(key = lambda x: x[3])
    info_ms.sort(key = lambda x: x[3])
    info_i2v.sort(key = lambda x: x[3])

    fout = codecs.open("precision_go_sort.txt","w",encoding="utf-8")
    for item in info_go:
        fout.write(str(item)+"\n")
    fout.close()
    fout = codecs.open("precision_ms_sort.txt","w",encoding="utf-8")
    for item in info_ms:
        fout.write(str(item)+"\n")
    fout.close()
    fout = codecs.open("precision_i2v_sort.txt","w",encoding="utf-8")
    for item in info_i2v:
        fout.write(str(item)+"\n")
    fout.close()

#precision()

def PCAPlot():
    import io, sys
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    tagset = set([])
#    tags = ["i2vtags","mstags","gotags"]
    tags = ["gotags"]
    for tag in tags:
        for item in anime:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                tagset.add(t)
        for item in jpop:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                tagset.add(t)
    idtag=list(tagset)
    idtag.sort()
    idtag = ["anime/jpop"]+idtag
    tagid = {}
    for id,tag in enumerate(idtag):
        tagid[tag]=id
    feature = np.zeros((len(jpop)*2,len(idtag)-1))
    cnt = 0
    for item in anime[:len(jpop)]:
        for tag in tags:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                feature[cnt][tagid[t]-1]=st[1]
        cnt+=1
    for item in jpop:
        for tag in tags:
            for st in item[tag]:
                t = tag+"_"+st[0].replace(" ","_")
                feature[cnt][tagid[t]-1]=st[1]
        cnt+=1
    from sklearn.decomposition import PCA
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
#    pca = PCA(n_components=2)
#    xtr = pca.fit_transform(feature)
#    plt.scatter(xtr[:len(jpop),0],xtr[:len(jpop),1],color="red",label="anime")
#    plt.scatter(xtr[len(jpop):,0],xtr[len(jpop):,1],color="blue",label="jpop")
#    plt.legend()
#    plt.show()
    target = [0]*len(jpop)+[1]*len(jpop)
    xtr1,xte1,ytr1,yte1 = train_test_split(feature[:len(jpop)],[0]*len(jpop),test_size=0.2)
    xtr2,xte2,ytr2,yte2 = train_test_split(feature[len(jpop):],[1]*len(jpop),test_size=0.2)
    xtr = list(xtr1)+list(xtr2)
    xte = list(xte1)+list(xte2)
    ytr = list(ytr1)+list(ytr2)
    yte = list(yte1)+list(yte2)
    lda = LinearDiscriminantAnalysis()
    ytrp = lda.fit_transform(xtr,ytr)
    ytep = lda.transform(xte)
    print(lda.score(xtr,ytr),lda.score(xte,yte))
    plt.subplot(2,1,1)
    plt.hist(ytrp[:len(ytrp)/2],normed=True,bins=50,alpha=0.3,label="anime",color="red")
    plt.hist(ytrp[len(ytrp)/2:],normed=True,bins=50,alpha=0.3,label="jpop",color="blue")
    plt.xlabel("train")
    plt.legend()
    plt.subplot(2,1,2)
    plt.hist(ytep[:len(ytep)/2],normed=True,bins=50,range=(-20,20),alpha=0.3,label="anime",color="red")
    plt.hist(ytep[len(ytep)/2:],normed=True,bins=50,range=(-20,20),alpha=0.3,label="jpop",color="blue")
    plt.xlabel("test")
    plt.legend()
    plt.savefig("lda.png")
    plt.show()
PCAPlot()
