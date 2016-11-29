import bottlenose
import pickle
import time
from bs4 import BeautifulSoup

from PIL import Image
import requests
from io import BytesIO

fin = open("./../../key/amazon.apikey")
AWSAccessKeyId=fin.readline().strip()
AWSSecretKey=fin.readline().strip()
AssocId = fin.readline().strip()
fin.close()

amazon = bottlenose.Amazon(AWSAccessKeyId, AWSSecretKey,AssocId,Region='JP')
response = amazon.ItemSearch(Keywords="test", SearchIndex="Music")
time.sleep(1.5)

soup = BeautifulSoup(response,"lxml")
items = soup.find("items")
print("{0} found".format(soup.find("totalresults").contents[0]))

c=1
for item in soup.findAll("item"):
    itemid = item.asin.contents[0]
    title = item.title.contents[0]
    print(itemid,item.artist.contents,title)
    res2 = amazon.ItemLookup(ItemId=itemid,SeachIndex="Music",ResponseGroup="Images")
    soup2 = BeautifulSoup(res2,"lxml")
    img = soup2.find("largeimage")
    if(img is not None):
        url = img.find("url").string
        print(url)
        res3 = requests.get(url)
        img = Image.open(BytesIO(res3.content))
        img.save("img{0}.{1}".format(c,url.split(".")[-1]))
    else:
        print("no image")
    time.sleep(1.5)

    c+=1
    if(c>=3):
        break
