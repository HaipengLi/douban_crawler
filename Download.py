import requests
import re
import random
import time
from ipPoolGenrator import IPPool

# 创建一个反反爬的类
class Download:
  def __init__(self):
    self.ipList = IPPool  ##初始化一个list用来存放获取到的ip
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

  def get(self, url, timeout=3, proxy=None, num_retries=6):  ##给函数一个默认参数proxy为空,默认num_retries为6次
    UA = random.choice(self.user_agent_list)  ##从user_agent_list中随机取出一个字符串。
    headers = {'User_Agent': UA}  ##构造一个完整的User_Agent
    if proxy == None:  ##当代理为空时，不使用代理获取response
      try:
        return requests.get(url, headers=headers)  ##返回一个requests.get的页面文件，调用随机的headers，服务器以为我们是真的浏览器了
      except:  ##如果上面的代码执行报错则执行下面的代码
        if num_retries > 0:  ##num_retries是限定的重试次数
          time.sleep(10)  ##延迟10秒
          print(u'获取网页出错，10s后将获取倒数第：', num_retries, u'次')
          return self.get(url, timeout, num_retries - 1)  ##调用自身，并减1，实现循环6次
        else:
          print(u'开始使用代理')
          time.sleep(10)
          IP = 'http://{}'.format(':'.join(random.choice(self.ipList)))  ##将从self.iplist中随机获取的字符串处理成需要的格式。去除两边空格后，用join拼接？
          proxy = {'http': IP}
          return self.get(url, timeout, proxy)  ##代理不为空的时候

    else:  ##当代理不为空
      try:
        IP = 'http://{}'.format(':'.join(random.choice(self.ipList)))  ##将从self.iplist中随机获取的字符串处理成需要的格式。去除两边空格后，用join拼接？
        proxy = {'http': IP}  ##构造成一个代理
        return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)  ##使用代理获取response
      except:
        if num_retries > 0:
          time.sleep(10)
          IP = ''.join(str(random.choice(self.ipList)).strip())
          proxy = {'http': IP}
          print(u'正在更换代理，10s后将重新获取倒数第', num_retries, u'次')
          print(u'当前代理是：', proxy)
          return self.get(url, timeout, proxy, num_retries - 1)
        else:
          print(u'代理也不好使！取消代理')
          return self.get(url, 3)


down = Download()