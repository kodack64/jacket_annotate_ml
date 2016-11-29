
import pickle
import matplotlib.pyplot as plt
import random
from gensim import corpora
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
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
    for c in getColorSet():
        print(c,getColorRatio(c))

#checkColor()

###################################################################################################

def checkRate():
    px = []
    py = []
    random.shuffle(anime)
    random.shuffle(jpop)
    for item in anime[:min(len(anime),len(jpop))]:
        px.append(item["i2vrate"][0][1])
        py.append(item["i2vrate"][1][1])
    plt.scatter(px,[0]*len(px),c="red",label="anime")

    px = []
    py = []
    for item in jpop[:min(len(anime),len(jpop))]:
        px.append(item["i2vrate"][0][1])
        py.append(item["i2vrate"][1][1])
    plt.scatter(px,[1]*len(px),c="blue",label="jpop")
    plt.legend()
    plt.show()
#checkRate()

###################################################################################################

def getCategorySet():
    catset = set([])
    for item in anime:
        for c in item["categories"]:
            try:
                catset.add(c["name"])
            except:
                pass
    for item in jpop:
        for c in item["categories"]:
            try:
                catset.add(c["name"])
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
                    if(cat in c["name"]):
                        ca+=1
                except:
                    pass
        for item in jpop:
            for c in item["categories"]:
                try:
                    if(cat in c["name"]):
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
    for item in anime:
        if(len(item["gotags"])>0):
            pack = []
            for st in item["gotags"]:
                st = st.replace(" ","")
                tagset.add(st)
                pack.append(st)
            corp_anime.append(" ".join(pack))
    for item in jpop:
        if(len(item["gotags"])>0):
            pack = []
            for st in item["gotags"]:
                st = st.replace(" ","")
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


    param = {"n_estimators" : list(range(20,40,1)), "max_depth":[2,3,4]}
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

    tagset = set([])
    for item in anime:
        if(len(item["gotags"])>0):
            pack = []
            for st in item["gotags"]:
                st = st.replace(" ","")
                tagset.add(st)
                pack.append(st)
            corp_anime.append(" ".join(pack))
    for item in jpop:
        if(len(item["gotags"])>0):
            pack = []
            for st in item["gotags"]:
                st = st.replace(" ","")
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
    print("\n".join(list(map(str,feats))[:20]))
    feats.reverse()
    print("\n".join(list(map(str,feats))[:20]))

#    feats = [[abs(rf.coef_[0][i]),rf.coef_[0][i],v,getIdKey(v)] for i,v in enumerate(supIndex)]
#    feats.sort()
#    print("\n".join(list(map(str,feats))[::-1]))
linearSep()
