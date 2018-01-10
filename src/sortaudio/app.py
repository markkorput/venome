from optparse import OptionParser
from pydub import AudioSegment
import numpy as np
import time, math

class Timer:
  def __init__(self, text='timer'):
    self.text = text

  def start(self):
    self.startTime = time.time()
    return self

  def end(self):
    print('{} ({} seconds)'.format(self.text, time.time()-self.startTime))

class Chunk:
  def __init__(self, frames, startFrame, originalIndex, sortedIndex=None, volume=None):
    self.frames = frames
    self.startFrame = startFrame
    self.originalIndex = originalIndex
    self.volume = volume
    self.sortedIndex = sortedIndex

class App:
  def __init__(self, opts={}):
    self.opts = opts
    self.load(self.opts.infile)
    self.process(float(self.opts.chunkSize)*1000)
    self.export(self.opts.infile+'.mp3')
    self.running=False # True

  def load(self, filepath):
    print('loading audio file: {}...'.format(filepath), end='')
    t1 = time.time()

    self.audioSegment = AudioSegment.from_file(filepath)
    # self.audio.channels # => 2
    # self.audio.sample_width # => 2 (2 bytes / sample?)
    # self.audio.frame_width # => 4 (4 bytes / frame; channelsxsample_width)
    # len(self.audio._data) # 5196544
    # len(self.audio.get_array_of_samples()) # 2598272 (samples for one channel?)
    # self.audio.frame_count() # 1299136.0 == len(self.audio._data) / self.audio.frame_width
    # self.audio.frame_rate # 44100 Hz
    # self.audio.duration_seconds # 29.45886621315193

    # self.samples = np.fromstring(self.audio._data, np.int16)
    # data = audio.get_array_of_samples()
    print(' done ({} seconds)'.format(time.time()-t1))

  def process(self, chunkMs):

    timer = Timer('getChunks').start()
    chunks = App.getChunks(self.audioSegment, chunkMs)
    timer.end()

    timer = Timer('populateVolumes').start()
    App.populateVolumes(chunks, self.audioSegment.frame_width)
    timer.end()

    # timer = Timer('populateSortedIndices').start()
    # App.populateSortedIndices(chunks)
    # timer.end()

    timer = Timer('applySortedChunks').start()
    App.applySortedChunks(self.audioSegment, chunks)
    timer.end()

  def export(self, filepath):
    print('exporting audio file: {}...'.format(filepath), end='')
    t1 = time.time()
    self.audioSegment.export(filepath)
    print(' done ({} seconds)'.format(time.time()-t1))

  def destroy(self):
    pass

  def update(self):
    pass

  def getChunks(audioSegment, chunkMs):
    chunkFrameCount = int(audioSegment.frame_count(chunkMs))
    totalFrameCount = audioSegment.frame_count()
    chunkCount = int(math.ceil(totalFrameCount / chunkFrameCount))

    chunks = []
    for i in range(chunkCount):
      startFrame = int(i * chunkFrameCount)
      endFrame = startFrame + chunkFrameCount
      frames = []
      for frameidx in range(startFrame, startFrame + chunkFrameCount):
        fr = audioSegment.get_frame(frameidx)
        # print('type: '+str(type(fr))) # => bytes
        frames.append(fr)

      print('got chunk {}/{}'.format(i+1, chunkCount), end='\r')
      chunks.append(Chunk(frames, startFrame, i))

    return chunks

  def populateVolumes(chunks, frameWidth):
    for i, chunk in enumerate(chunks):
      # frameCount = len(chunk.data) / frameWidth
      # for frame in np.array(chunk.data).reshape(frameCount, frameWidth)

      chunkSum = 0

      if len(chunk.frames) > 0:
        for frame in chunk.frames:
          for byte in frame:
            chunkSum += byte
        chunk.volume = chunkSum / len(chunk.frames)
        print('volume of chunk {}/{}: {}'.format(i+1, len(chunks), chunk.volume), end='\r')

  # def populateSortedIndices(chunks):
  #   loudestFirstList = sorted(chunks, key=lambda x: x.volume, reverse=True)
  #   for i, chunk in enumerate(loudestFirstList):
  #     chunk.sortedIndex = i
  #     print('sorted chunk {}/{}'.format(i+1, len(chunks)), end='\r')

  def applySortedChunks(audioSegment, chunks):
    data = bytearray([])

    loudestFirstList = sorted(chunks, key=lambda x: x.volume, reverse=True)
    for i, chunk in enumerate(loudestFirstList):
      for frame in chunk.frames:
        data.extend(frame)

      print('applied chunk {}/{}'.format(i+1, len(chunks)), end='\r')

    audioSegment._data = bytes(data)

if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-v', '--verbose', dest='verbose', action="store_true", default=False)
  parser.add_option('-i', '--in-file', dest='infile', default='data/test.ogg')
  parser.add_option('-s', '--chunksize', dest='chunkSize', default=1)
  # parser.add_option('-o', '--out-file', dest='outfile', default=None)
  # parser.add_option('-y', '--yml', '--yaml', '--config-file', dest='config_file', default=None)

  opts, args = parser.parse_args()

  app = App(opts)

  try:
      while app.running:
          app.update()
  except KeyboardInterrupt:
      print('KeyboardInterrupt. Quitting.')

  app.destroy()
