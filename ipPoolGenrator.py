"""
crawler free proxy ip from http://www.xicidaili.com and test validity
"""
import telnetlib, requests, time
from lxml import html
from mongoengine import *
MAX_TIME_LENGTH=3600 # the max length of time that we have to update ip pool
connect('ip_pool')
class ipRecord(Document):
  pin=IntField(required=True,unique=True)
  ipAndPort=ListField(required=True)
  updateTime=IntField(required=True)
headers = {
  "Host": "www.xicidaili.com",
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

def isValidProxy(ip,port):
  try:
    print("testing {}:{}...".format(ip,port),end="")
    telnetlib.Telnet(ip, port=port, timeout=2)
  except:
    print("Failed")
    return False
  else:
    print("Succeed")
    return True
def crawlIP(pages=2):
    ips=[]
    ports=[]
    for i in range(pages):
        print("page {} ...".format(str(i+1)))
        res=requests.get("http://www.xicidaili.com/nn/{}".format(i+1),headers=headers)
        time.sleep(2)
        tree=html.fromstring(res.text)
        ips += tree.xpath('//tr/td[position()=2]/text()') # or td[2]
        ports += tree.xpath('//tr/td[position()=3]/text()')
    return zip(ips,ports)
def generate(rawIPZip):
    IPPool=[]
    for ip,port in rawIPZip:
        if isValidProxy(ip,port):
            IPPool.append((ip,port))
    return IPPool
try:
  iprecord=ipRecord.objects.get(pin=0)
except:
  # create one
  print("creating ip pool...")
  iprecord = ipRecord(pin=0,ipAndPort=generate(crawlIP(1)),updateTime=int(time.time()))
  iprecord.save()
else:
  if MAX_TIME_LENGTH<int(time.time())-iprecord.updateTime:
    # update
    print("updating ip pool...")
    iprecord.ipAndPort=generate(crawlIP(1))
    iprecord.save()
  else:
    # keep
    print("use ip pool in database")
    pass
IPPool=iprecord.ipAndPort
if __name__=='__main__':
  print("ip count: {}".format(len(IPPool)))