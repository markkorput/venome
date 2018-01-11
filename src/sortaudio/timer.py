import time

class Timer:
  def __init__(self, text='timer'):
    self.text = text
    self.startTime = time.time()

  def end(self):
    print('{} ({} seconds)'.format(self.text, time.time()-self.startTime))
