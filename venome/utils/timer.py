import time

class Timer:
  def __init__(self, text='timer', postfix=None):
    self.text = text
    self.startTime = time.time()
    self.postfix = postfix

  def end(self):
    print('{} -- END ({} seconds)'.format(self.text, time.time()-self.startTime))
    if self.postfix:
      print(self.postfix)

  def __enter__(self):
    print('{} -- START'.format(self.text))
    if self.postfix:
      print(self.postfix)

  def __exit__(self, type, value, traceback):
    self.end()

if __name__ == '__main__':
  with Timer('test'): # as t:
    print('during')
