from optparse import OptionParser
import numpy as np
import subprocess, os
from pydub import AudioSegment
from .utils.timer import Timer






if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-i', '--in-file', dest='infile', default='data/test.mp4')
  parser.add_option('-o', '--out-file', dest='outfile', default=None)
  parser.add_option('-s', '--chunk-size', dest='chunk_size', default=1) # seconds
  parser.add_option('-f', '--fps', dest='fps', default=25) # TODO: default to infile's fps
  parser.add_option('-w', '--work-folder-postfix', dest='workfolder_postfix', default='auto')
  parser.add_option('--vcodec', dest='vcodec', default='libx264')
  parser.add_option('--pix_fmt', dest='pix_fmt', default='yuv420p')
  parser.add_option('--audio-postfix', dest='audio_postfix', default='_audio.mp3')
  parser.add_option('--sorted-audio-filename', dest='sorted_audio_filename', default='audio.mp3')
  parser.add_option('--frames-postfix', dest='frames_postfix', default='_frames/f%d.png')
  parser.add_option('--chunk-filename', dest='chunk_filename', default='chunks.json.txt')
  parser.add_option('--no-audio-cleanup', dest='audio_cleanup', action='store_false', default=True)
  parser.add_option('--no-frames-cleanup', dest='frames_cleanup', action='store_false', default=True)
  parser.add_option('--no-workfolder-cleanup', dest='workfolder_cleanup', action='store_false', default=True)
  parser.add_option('--no-clean', dest='any_clean', action='store_false', default=True)

  # parser.add_option('-y', '--yml', '--yaml', '--config-file', dest='config_file', default=None)
  opts, args = parser.parse_args()

  bCleanFrames = opts.frames_cleanup
  bCleanWorkFolder = opts.workfolder_cleanup
  workFolder = opts.infile+('_chunksort_volume_chunksize{}'.format(opts.chunk_size) if opts.workfolder_postfix == 'auto' else foropts.workfolder_postfix)
  audioFilePath = opts.infile+opts.audio_postfix
  framesPath = opts.infile+opts.frames_postfix
  sortedFramesPath = os.path.join(workFolder, 'frames', 'f{:d}.png')
  sortedAudioFilePath = os.path.join(workFolder, opts.sorted_audio_filename)
  chunksFilePath = os.path.join(workFolder, opts.chunk_filename)
  outFile = opts.outfile if opts.outfile != None else opts.infile+'_chunksort_volume_chunksize{}.mp4'.format(opts.chunk_size)
  anyClean = opts.any_clean
  fps = opts.fps

  with Timer('\n[EXTRACT AUDIO]', postfix='\n'):
    dirname = os.path.dirname(audioFilePath)
    if not os.path.isdir(dirname):
      os.makedirs(dirname)

    if subprocess.run(['ffmpeg', '-i', opts.infile, audioFilePath]).returncode != 0:
      anyClean = False

  with Timer('\n[SPLIT VIDEO INTO FRAMES]', postfix='\n'):
    dirname = os.path.dirname(framesPath)
    if not os.path.isdir(dirname):
      os.makedirs(dirname)
      # ffmpeg -i data/video.mp4 -vf fps=25 data/video.mp4.frames/f%d.png
      if subprocess.run(['ffmpeg', '-i', opts.infile, framesPath]).returncode != 0:
        anyClean = False
    else:
      # TODO: prompt user for (re-)generate?/
      print('FRAMES FOLDER ALREADY EXISTS, ASSUMING FRAMES WERE ALREADY GENERATED')
      if bCleanFrames:
        print('\n!! Video frames target folder already exists, frames-cleanup disabled !!')
        bCleanFrames = False

  with Timer('\n[SORT AUDIO]', postfix='\n'):
    if os.path.isfile(sortedAudioFilePath) and os.path.isfile(chunksFilePath):
      print('both sorted audio file and chunks file already exist, skipping audio sorting')
    else:
      if not os.path.isdir(os.path.dirname(sortedAudioFilePath)):
        os.makedirs(os.path.dirname(sortedAudioFilePath))

      if not os.path.isdir(os.path.dirname(chunksFilePath)):
        os.makedirs(os.path.dirname(chunksFilePath))

      if subprocess.run(['python',
        '-m', 'venome.sortaudio.app',
        '--chunksize', str(opts.chunk_size),
        '-i', audioFilePath,
        '-o', sortedAudioFilePath,
        '-c', chunksFilePath]).returncode != 0:
        anyClean = False

  with Timer('\n[SORT FRAMES]', postfix='\n'):
    if not os.path.isdir(os.path.dirname(sortedFramesPath)):
      os.makedirs(os.path.dirname(sortedFramesPath))

    if subprocess.run(['python',
      '-m', 'venome.sortframes',
      '-c', chunksFilePath,
      '--fps', str(fps),
      '-i', framesPath.replace('%d', '{:d}'),
      '-o', sortedFramesPath]).returncode != 0:
      anyClean = False

  with Timer('\n[CREATE MOVIE FILE]'.format(outFile, sortedFramesPath.replace('{:d}', '%d')), postfix='\n'):
    if not os.path.isdir(os.path.dirname(outFile)):
      os.makedirs(os.path.dirname(outFile))
    cmd = ['ffmpeg',
        '-r', str(fps),
        '-f', 'image2',
        '-i', sortedFramesPath.replace('{:d}', '%d'),
        '-i', sortedAudioFilePath,
        '-vcodec', opts.vcodec,
        '-crf', str(fps),
        '-pix_fmt', opts.pix_fmt,
        '-acodec', 'copy',
        outFile]
    print('cmd: {}'.format(' '.join(cmd)))
    if subprocess.run(cmd).returncode != 0:
      anyClean = False

  if anyClean and opts.audio_cleanup:
    with Timer('\n[CLEANING UP EXTRACTED AUDIO]', postfix='\n'):
      subprocess.run(['rm', audioFilePath])

  if anyClean and bCleanFrames:
    with Timer('\n[CLEANING UP EXTRACTED FRAMES]', postfix='\n'):
      subprocess.run(['rm', '-rf', os.path.dirname(opts.infile+opts.frames_postfix)])

  if anyClean and bCleanWorkFolder:
    with Timer('\n[CLEANING UP WORK FOLDER]', postfix='\n'):
      subprocess.run(['rm', '-rf', workFolder])
