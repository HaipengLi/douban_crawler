from lxml import html
import os
import time
from mongoengine import *
from test_db import albumRecord,userRecord
from Download import down
connect('douban_album')
# todo save albumList & photoList in DB
# todo save IP in DB  bug: use wrong db to store ip pool !
# todo use another ip pool when none of them is available
def getAllPhotoInAlbum(albumLink,title):
  photoList=[]
  albumID=int(link.split('/')[-2])
  i=0
  while True:
    print('get photo link at page '+str(i)+ '...')
    page=down.get(albumLink)
    time.sleep(1)
    tree=html.fromstring(page.text)
    photoList+=tree.xpath('//a[@class="photolst_photo"]/@href')
    try:
      albumLink=tree.xpath('//link[@rel="next"]/@href')[0]
      i+=1
    except IndexError:
      break
  for i,photo in enumerate(photoList):
    picID=photo.split('/')[-2]
    #pic filter
    try:
      albumRecord.objects.get(albumID=albumID, picID=picID)
    except DoesNotExist:
      #crawl
      # and record
      temp = albumRecord(albumID=albumID, picID=picID)
      user.album.append(temp)
      temp.save()
    else:
      # visited
      continue
    photoURL='https://img3.doubanio.com/view/photo/l/public/p'+picID+'.webp'
    try:
      os.mkdir(title)
    except FileExistsError:
      pass
    with open(title+'/'+str(i)+'.webp','wb') as f:
      print('get '+photoURL+' of album "'+title+'"...')
      f.write(down.get(photoURL).content)
      print('success\nwaiting...')
      time.sleep(1)
  print('done with album: '+title)

username='Forskolin'
link='https://www.douban.com/people/'+username
main_page = down.get(link)
#对获取到的page格式化操作，方便后面用XPath来解析
main_tree = html.fromstring(main_page.text)
#XPath解析，获得你要的文字段落！
name = main_tree.xpath('//div[@class="user-info"]/div[@class="pl"]/text()')[0].strip()
intro = main_tree.xpath('//span[@id="intro_display"]/text()')

photo_link=link.rstrip('/')+'/photos'

try:
  os.mkdir('data')
except FileExistsError:
  pass
os.chdir('data')
try:
  os.mkdir(name)
except FileExistsError:
  pass
os.chdir(name)
try:
  os.mkdir('albums')
except FileExistsError:
  pass
os.chdir('albums')

# db
try:
  user=userRecord.objects.get(username=username)
except DoesNotExist:
  # not found -> create one
  user = userRecord(username=username)
  user.save()

albumDict={}
i=0
while True:
  print('get album link at page '+str(i)+'...')
  photo_page = down.get(photo_link)
  time.sleep(1)
  photo_tree=html.fromstring(photo_page.text)
  albumList=photo_tree.xpath('//div[@class="wr"]/div[@class="albumlst"]')
  for album in albumList:
    link=album.xpath('.//div[@class="pl2"]/a/@href')[0]
    #album filter
    total=int(album.xpath('.//span[@class="pl"]/text()')[0].split('张')[0].strip()) # get the total number of pictures of an album
    albumID=int(link.split('/')[-2])
    title = album.xpath('.//div[@class="pl2"]/a/text()')[0]
    if total == albumRecord.objects(albumID=albumID).count():
      print("jump album {}".format(title))
      continue  # next album
    else:
      # not finished album
      pass
    albumDict[title]=link
  try:
    i+=1
    photo_link=photo_tree.xpath('//link[@rel="next"]/@href')[0]
  except IndexError: # the end of album page
    break

for title,link in dict.items(albumDict):
  getAllPhotoInAlbum(link,title)

os.chdir('../../..')
# test
