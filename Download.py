import requests
import re
import random
import time
from IPPoolGenrator import IPPool,isExpired, regenerate
from MyLog import *

# Anti Anti http requests
class Download:
  def __init__(self):
    # list of IP:port
    self.ipList = IPPool
    self.user_agent_list = [
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
      "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
      "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

  def get(self, url, timeout=3, proxy=None, num_retries=6):
    # random choose a user-agent
    UA = random.choice(self.user_agent_list)
    headers = {'User_Agent': UA} 
    if isExpired:
      self.ipList=regenerate()
    # do not use proxy
    # use user's ip
    if proxy == None: 
      try:
        return requests.get(url, headers=headers)
      except:
        # if requests failed
        if num_retries > 0: 
          # delay 10 seconds and try again
          time.sleep(10)
          # retry by call self
          return self.get(url, timeout, num_retries - 1)
        else:
          printWithTime(u'Use Proxy')
          time.sleep(10)
          # random choose a ip from ip pool
          IP = 'http://{}'.format(':'.join(random.choice(self.ipList)))
          proxy = {'http': IP}
          return self.get(url, timeout, proxy)
    else:
      # use proxy
      try:
        IP = 'http://{}'.format(':'.join(random.choice(self.ipList)))
        proxy = {'http': IP} 
        return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
      except:
        if num_retries > 0:
          time.sleep(10)
          IP = ''.join(str(random.choice(self.ipList)).strip())
          proxy = {'http': IP}
          return self.get(url, timeout, proxy, num_retries - 1)
        else:
          return self.get(url, 3)


down = Download()