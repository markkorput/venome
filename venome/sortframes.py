from optparse import OptionParser
import shutil, json
import os.path
from .utils.timer import Timer
from .utils.lines_file import LinesFile

class App:
  def __init__(self, opts):
    self.opts = opts
    self.frameCursor = 0

    timer = Timer('detectFirstInFileNumber: {}'.format(self.opts.chunkfile))
    self.firstInFileNumber = App.detectFirstInFileNumber(self.opts.infile)
    timer.end()

    if self.firstInFileNumber == None:
      print('Could not find first in-file for pattern: {}'.format(self.opts.infile))
    else:
      timer = Timer('processing chunk file: {}'.format(self.opts.chunkfile))
      App.process(self.opts.chunkfile, self.applyChunk)
      timer.end()

    self.running = False

  def process(filepath, chunkApply):
    if not filepath or filepath == '':
      print('not chunk file specified')
      return

    f = LinesFile(filepath)
    while True:
      line = f.nextLine()
      if not line:
        break # done

      data = json.loads(line)
      # print('got schucnk:', data)
      chunkApply(data['startTime'], data['duration'])

  def detectFirstInFileNumber(infile):
    for i in range(101):
      if os.path.isfile(infile.format(i)):
        return i
    return None

  def applyChunk(self, startTime, duration):
    fps = float(self.opts.fps)

    startFrame = int(startTime * fps)
    frameCount = int(duration * fps)

    for idx in range(startFrame, startFrame + frameCount + 1):
      if self.processFrame(self.frameCursor, idx):
        self.frameCursor += 1

  def processFrame(self, newIndex, originalIndex):
    infile = self.opts.infile
    outfile = self.opts.outfile

    inpath = infile.format(self.firstInFileNumber + originalIndex)
    outpath = outfile.format(newIndex)

    if not os.path.isfile(inpath):
      print('COULD NOT FIND FRAME FILE: {}'.format(inpath))
      return False

    shutil.copy(inpath, outpath)
    return True

  def destroy(self):
    pass

  def update(self):
    pass

if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-v', '--verbose', dest='verbose', action="store_true", default=False)
  parser.add_option('-f', '--fps', dest='fps', default=25)
  parser.add_option('-c', '--chunk-file', dest='chunkfile', default=None)
  parser.add_option('-i', '--in-file', dest='infile', default='data/frames/out{:d}.png')
  parser.add_option('-o', '--out-file', dest='outfile', default='data/frames/resorted_out{:d}.png')

  opts, args = parser.parse_args()
  app = App(opts)

  try:
      while app.running:
          app.update()
  except KeyboardInterrupt:
      print('KeyboardInterrupt. Quitting.')

  app.destroy()
