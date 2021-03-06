from tqdm import tqdm
import os,sys,time
from lxml import html
from mongoengine import *
from PIL import Image

from DBDefine import albumRecord,userRecord
from MyLog import *
from Download import down
# todo jump certain album
# todo: fail to recognise visited album
# todo save IP in DB  bug: use wrong db to store ip pool !
# todo add tools to convert .webp to .jpg
def getAllPhotoInAlbum(albumLink,title,total):
  photoIDList=[]
  albumID=int(albumLink.split('/')[-2])
  i=0
  printWithTime('{} begin...'.format(title))
  # if all in db (including status==False)
  if total == albumRecord.objects(albumID=albumID).count():
    pass # jump collecting
  else:
    # else continue collecting (add those not in db)
    while True:
      printWithTime('get photo link at page ' + str(i) + '...')
      page = down.get(albumLink)
      time.sleep(1)
      tree = html.fromstring(page.text)
      photoListInOnePage=tree.xpath('//a[@class="photolst_photo"]/@href')
      for photo in photoListInOnePage:
        picID = photo.split('/')[-2]
        try:
          albumRecord.objects.get(albumID=albumID, picID=picID)
        except: # if not in db, add
          temp = albumRecord(albumID=albumID, picID=picID, status=False)
          temp.save()
        else: # already in db, jump
          continue
      try:
        albumLink = tree.xpath('//link[@rel="next"]/@href')[0]
        if albumLink[-3:]=='sep': # in order to distinguish the 'next page' of album from the 'next page' of reviews
          break
        i += 1
      except IndexError:
        break
  for queryResult in albumRecord.objects(albumID=albumID, status=False):
    photoIDList.append(queryResult['picID'])
  # todo display percentage
  for i,picID in enumerate(tqdm(photoIDList)):
    # #pic filter
    # try:
    #   albumRecord.objects.get(albumID=albumID, picID=picID)
    # except DoesNotExist:
    #   #crawl
    #   # and record
    #   temp = albumRecord(albumID=albumID, picID=picID)
    #   # todo append album to user (error in python3.5, non local variable)
    #   # user.album.append(temp)
    #   temp.save()
    # else:
    #   # visited
    #   continue
    photoURL='https://img3.doubanio.com/view/photo/l/public/p{}.webp'.format(picID)
    try:
      os.mkdir(title)
    except FileExistsError:
      pass
    filename = title+'/'+str(picID)+'.webp'
    with open(filename,'wb') as f:
      print('Download '+photoURL.split('/')[-1]+' of album "'+title)
      f.write(down.get(photoURL).content)
    temp_img = Image.open(filename).convert("RGB")
    temp_img.save(title+'/'+str(picID)+'.jpg')
    os.remove(filename)
    time.sleep(1)
    # update status to True
    albumRecord.objects(albumID=albumID, picID=picID).update_one(status=True)
  printWithTime('done with album: '+title)
def main():
  if (len(sys.argv) > 1):
    username = sys.argv[1]
  else:
    username=input('type the username you want to crawl: ')
  printWithTime('connecting database...')
  connect('douban_album')
  link='https://www.douban.com/people/'+username
  # http get
  main_page = down.get(link)
  # parse
  main_tree = html.fromstring(main_page.text)
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
    printWithTime('get album link at page '+str(i)+'...')
    photo_page = down.get(photo_link)
    time.sleep(1)
    photo_tree=html.fromstring(photo_page.text)
    albumList=photo_tree.xpath('//div[@class="wr"]/div[@class="albumlst"]')

    for album in albumList:
      link=album.xpath('.//div[@class="pl2"]/a/@href')[0]
      title = album.xpath('.//div[@class="pl2"]/a/text()')[0]
      #album filter
      total = int(album.xpath('.//span[@class="pl"]/text()')[0].split('张')[0].strip())  # get the total number of pictures of an album
      albumID = int(link.split('/')[-2])
      if total == albumRecord.objects(albumID=albumID,status=True).count():
        printWithTime("jump album {}".format(title))
        continue  # next album
      else:
        # not finished album
        pass
      albumDict[title]=[link,total]
    try:
      i+=1
      photo_link=photo_tree.xpath('//link[@rel="next"]/@href')[0]
    except IndexError: # the end of album page
      break

  for title,linkAndTotal in dict.items(albumDict):
    getAllPhotoInAlbum(linkAndTotal[0],title,linkAndTotal[1])
  printWithTime("Mission Complete!")
  os.chdir('../../..')
# test
if __name__=='__main__':
  main()