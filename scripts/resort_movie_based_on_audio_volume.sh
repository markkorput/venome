# split extract audo file from movie
ffmpeg -i data/test.mp4 data/test.mp4_audio.mp3

# split video into separate frame file
ffmpeg -i data/video.mp4 -vf fps=25 data/video.mp4.frames/f%d.png

# generated sorted audio file and chunks sorting data file
# python -m venome.sortaudio.app
#  -i data/audio.ogg
#  -o data/sorted/audio.ogg.mp3
#  --chunksize 2
#  -c chunks.txt
python -m venome.sortaudio.app --chunksize 2 -i data/sorted/test.mp4_audio.mp3 -o data/sorted/test.mp4_audio.mp3-sorted.mp3 -c data/sorted/chunks.txt

# resort frames using generated chunk file
# python -m venome.sortframes
#   -c chunks.txt
#   --fps 25
#   -i data/video.mp4.frames/f{:d}.png
#   -o frame/sorted{:d}.png
python -m venome.sortframes -c data/sorted/chunks.txt --fps 25 -i data/test.mp4_frames/out{:d}.png -o data/sorted/frames/f{:d}.png

# convert frames to movie
# http://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/
ffmpeg -r 25 -f image2 -i data/sorted/frames/f%d.png -i data/sorted/test.mp4_audio.mp3-sorted.mp3 -vcodec libx264 -crf 25 -pix_fmt yuv420p -acodec copy data/sorted/test.mp4
# without audio
ffmpeg -r 25 -f image2 -i data/sorted/frames/f%d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p data/sorted/test.mp4
