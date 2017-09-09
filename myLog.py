import time
def logTime(func):
  def decorator(*args, **kwargs):
    print(time.strftime("[%d/%m/%Y %H:%M:%S] "),end='')
    return func(*args,**kwargs)
  return decorator
@logTime
def printWithTime(*args, **kwargs):
  print(*args, **kwargs)
