"""
crawler free proxy ip from http://www.xicidaili.com and test validity
"""
import telnetlib, requests, time
from lxml import html
from mongoengine import *
from myLog import *
MAX_TIME_LENGTH=3600 # the max length of time that we have to update ip pool
class ipRecord(Document):
  pin=IntField(required=True,unique=True)
  ipAndPort=ListField(required=True)
  updateTime=IntField(required=True)
def isValidProxy(ip,port):
  try:
    printWithTime("testing {}:{}...".format(ip,port),end="")
    telnetlib.Telnet(ip, port=port, timeout=2)
  except:
    printWithTime("Failed")
    return False
  else:
    printWithTime("Succeed")
    return True
def crawlIP(pages=2):
    ips=[]
    ports=[]
    for i in range(pages):
        printWithTime("page {} ...".format(str(i+1)))
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
connect('ip_pool')
headers = {
  "Host": "www.xicidaili.com",
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}
try:
  iprecord=ipRecord.objects.get(pin=0)
except:
  # create one
  printWithTime("creating ip pool...")
  iprecord = ipRecord(pin=0,ipAndPort=generate(crawlIP(1)),updateTime=int(time.time()))
  iprecord.save()
else:
  if MAX_TIME_LENGTH<int(time.time())-iprecord.updateTime:
    # update
    printWithTime("updating ip pool...(last time {} second(s) ago)".format(int(time.time())-iprecord.updateTime))
    iprecord.ipAndPort=generate(crawlIP(1))
    iprecord.updateTime=int(time.time())
    iprecord.save()
  else:
    # keep
    printWithTime("use ip pool in database")
    pass
IPPool=iprecord.ipAndPort
if __name__=='__main__':
  printWithTime("ip count: {}".format(len(IPPool)))