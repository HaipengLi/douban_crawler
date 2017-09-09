from pymongo import MongoClient
client = MongoClient()
albumDB = client['douban_album']
username='sixXXXXXXX'
album_collection=albumDB[username]
collectionData={}
albumID=1650850811


picID=2498370196
if picID in collectionData[albumID]:
  # next one
  pass
else:
  # crawl and record
  collectionData[albumID].append(picID)
  collectionData[albumID]['count']+=1