#-*-coding:utf-8-*- #编码声明，不要忘记！
import requests  #这里使用requests，小脚本用它最合适！
from lxml import html    #这里我们用lxml，也就是xpath的方法
from http import cookiejar
import os
import time
def getAllPhotoInAlbum(albumLink,title):
  photoList=[]
  while True:
    page=session.get(albumLink, headers=headers)
    tree=html.fromstring(page.text)
    photoList+=tree.xpath('//a[@class="photolst_photo"]/@href')
    try:
      albumLink=tree.xpath('//link[@rel="next"]/@href')[0]
    except:
      break
  for i,photo in enumerate(photoList):
    photoCode=photo.split('/')[-2]
    photoURL='https://img3.doubanio.com/view/photo/l/public/p'+photoCode+'.webp'
    try:
      os.mkdir(title)
    except FileExistsError:
      pass
    with open(title+'/'+str(i)+'.webp','wb') as f:
      print('get '+photoURL+'of album "'+title+'"...')
      f.write(requests.get(photoURL).content)
      print('success\nwaiting...')
      time.sleep(1)
  print('done with album: '+title)
headers = {
  "Host": "www.douban.com",
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
  print(session.cookies)
  session.cookies.load(ignore_discard=True)

except:
  print("还没有cookie信息")

link='https://www.douban.com/people/Forskolin/'
# main_page = session.get(link, headers=headers)
# #对获取到的page格式化操作，方便后面用XPath来解析
# main_tree = html.fromstring(main_page.text)
# #XPath解析，获得你要的文字段落！
# intro = main_tree.xpath('//span[@id="intro_display"]/text()')
# crawler self-intro
photo_link=link+'photos'

photo_page = session.get(photo_link, headers=headers)
photo_tree=html.fromstring(photo_page.text)
albumList=photo_tree.xpath('//div[@class="wr"]/div[@class="albumlst"]')
albumDict={}
for album in albumList:
  albumDict[album.xpath('.//div[@class="pl2"]/a/text()')[0]]=album.xpath('.//div[@class="pl2"]/a/@href')[0]

for title,link in dict.items(albumDict):
  getAllPhotoInAlbum(link,title)

# test
