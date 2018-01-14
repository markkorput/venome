from optparse import OptionParser
from pydub import AudioSegment
import numpy as np
import math, json
from .timer import Timer

class Chunk:
  def __init__(self, frames, startFrame, sortedIndex=None, volume=0.0):
    self.frames = frames
    self.startFrame = startFrame
    self.volume = volume
    self.sortedIndex = sortedIndex

  def startTime(self, fps):
    return self.startFrame / fps

  def duration(self, fps):
    return len(self.frames) / fps if self.frames else 0

class App:
  def __init__(self, opts={}):
    self.opts = opts

    self.load(self.opts.infile)
    self.process(float(self.opts.chunkSize)*1000, self.opts.chunkfile)
    self.export(self.opts.outfile if self.opts.outfile else self.opts.infile+'.mp3')

    self.running=False # True

  def load(self, filepath):
    timer = Timer('loading audio file: {}...'.format(filepath))
    self.audioSegment = AudioSegment.from_file(filepath)
    timer.end()

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

  def process(self, chunkMs, chunkfile=None):
    timer = Timer('getChunks')
    chunks = App.getChunks(self.audioSegment, chunkMs)
    timer.end()

    timer = Timer('populateVolumes')
    self.populateVolumes(chunks, self.audioSegment.frame_width)
    timer.end()

    # timer = Timer('populateSortedIndices')
    # App.populateSortedIndices(chunks)
    # timer.end()

    timer = Timer('applySortedChunks')
    App.applySortedChunks(self.audioSegment, chunks)
    timer.end()

    if chunkfile:
      timer = Timer('writeChunkFile to {}'.format(chunkfile))
      App.writeChunkFile(chunks, chunkfile, self.audioSegment.frame_rate)
      timer.end()

  def export(self, filepath):
    timer = Timer('exporting audio file: {}...'.format(filepath))
    self.audioSegment.export(filepath)
    timer.end()

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
      endFrame = int(min(startFrame + chunkFrameCount, totalFrameCount))
      frames = []
      for frameidx in range(startFrame, endFrame):
        fr = audioSegment.get_frame(frameidx)
        # print('type: '+str(type(fr))) # => bytes
        frames.append(fr)

      print('got chunk {}/{}'.format(i+1, chunkCount), end='\r')
      chunks.append(Chunk(frames, startFrame))

    return chunks

  def populateVolumes(self, chunks, frameWidth):
    for i, chunk in enumerate(chunks):
      if len(chunk.frames) > 0:
        for frame in chunk.frames:
          seg = AudioSegment(
            # raw audio data (bytes)
            data=frame,
            # 2 byte (16 bit) samples
            sample_width=self.audioSegment.sample_width,
            # 44.1 kHz frame rate
            frame_rate=self.audioSegment.frame_rate,
            # stereo
            channels=self.audioSegment.channels)
          # for byte in frame:
          #   chunkSum += byte
          chunk.volume += seg.dBFS
        chunk.volume /= len(chunk.frames)
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

  def writeChunkFile(chunks, chunkfile, frameRate):
    json_list = []

    loudestFirstList = sorted(chunks, key=lambda x: x.volume, reverse=True)
    for chunk in loudestFirstList:
      json_list.append(json.dumps({'startTime': chunk.startTime(frameRate), 'duration': chunk.duration(frameRate)}, separators=(',',':')))

    with open(chunkfile, 'w') as f:
      f.write('\n'.join(json_list))




if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-v', '--verbose', dest='verbose', action="store_true", default=False)
  parser.add_option('-i', '--in-file', dest='infile', default='data/test.ogg')
  parser.add_option('-s', '--chunksize', dest='chunkSize', default=1)
  parser.add_option('-c', '--chunk-file', dest='chunkfile', default=None)
  parser.add_option('-o', '--out-file', dest='outfile', default=None)
  # parser.add_option('-y', '--yml', '--yaml', '--config-file', dest='config_file', default=None)

  opts, args = parser.parse_args()

  app = App(opts)

  try:
      while app.running:
          app.update()
  except KeyboardInterrupt:
      print('KeyboardInterrupt. Quitting.')

  app.destroy()
