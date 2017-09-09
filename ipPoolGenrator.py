"""
crawler free proxy ip from http://www.xicidaili.com and test validity
"""
import telnetlib, requests, time
from lxml import html
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
IPPool=generate(crawlIP(1))
print(IPPool)