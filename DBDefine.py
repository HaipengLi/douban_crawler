from mongoengine import *

connect('douban_album')
class albumRecord(Document):
  albumID=IntField(required=True)
  picID=IntField(required=True,unique=True) # todo: use int or string?
  status=BooleanField(required=True,default=False)
class userRecord(Document):
  username=StringField(required=True,max_length=30,unique=True)
  album=ListField(ReferenceField(albumRecord))
def test():
  username='sixXXXXXXX'
  # user filter
  try:
    user=userRecord.objects.get(username=username)
  except DoesNotExist:
    # not found -> create one
    user = userRecord(username=username)
    user.save()
  # album filter
  albumID=1650850811
  total=2 # 2 pics in this album
  if total==albumRecord.objects(albumID=albumID).count(): # todo: can only search within this user?
    pass # next album
  else:
    # not finished album
    pass
  # pic filter
  picID=2498370196
  try:
    albumRecord.objects.get(albumID=albumID,picID=picID)
  except DoesNotExist:
    # todo: crawl
    # and record
    temp=albumRecord(albumID=albumID,picID=picID)
    user.album.append(temp)
    temp.save()
  else:
    # visited
    pass