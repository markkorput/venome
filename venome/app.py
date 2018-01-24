from optparse import OptionParser
from pydub import AudioSegment
import numpy as np
import time

class App:
  def __init__(self, opts={}):
    self.opts = opts
    self.audio = App.loadAudio(self.opts.infile)
    self.running=False #True

  def loadAudio(filepath):
    print('loading audio file: {}...'.format(filepath))
    t1 = time.time()

    audio = AudioSegment.from_file(filepath)
    # self.audio.channels # => 2
    # self.audio.sample_width # => 2 (2 bytes / sample?)
    # self.audio.frame_with # => 4 (4 bytes / frame; channelsxsample_width)
    # len(self.audio._data) # 5196544
    # len(self.audio.get_array_of_samples()) # 2598272 (samples for one channel?)
    # self.audio.frame_count() # 1299136.0 == len(self.audio._data) / self.audio.frame_width
    # self.audio.frame_rate # 44100 Hz
    # self.audio.duration_seconds # 29.45886621315193

    # self.samples = np.fromstring(self.audio._data, np.int16)
    data = audio.get_array_of_samples()
    print('done ({} seconds)'.format(time.time()-t1))
    return data

  def destroy(self):
    pass

  def update(self):
    pass



if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-v', '--verbose', dest='verbose', action="store_true", default=False)
  parser.add_option('-i', '--in-file', dest='infile', default='data/test.ogg')
  # parser.add_option('-y', '--yml', '--yaml', '--config-file', dest='config_file', default=None)

  opts, args = parser.parse_args()

  app = App(opts)

  try:
      while app.running:
          app.update()
  except KeyboardInterrupt:
      print('KeyboardInterrupt. Quitting.')

  app.destroy()
