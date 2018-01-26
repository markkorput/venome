inputdir='/Users/mark/Dropbox/Projects/AnalogDigital/_MEDIA'
outdir='./_render'
renderdir=$outdir'/test01-row-bars'


# mkdir $outdir
# mkdir $renderdir


### SPLIT ORIGINAL VIDEO INTO SEPARATE BAR IMAGE SEQUENCES
# mkdir $outdir/test01-row-bars
# NatronRenderer -b -w Write1 $renderdir/b0-f####.png 13-37 ./01-row.ntp
# NatronRenderer -b -w Write1 $renderdir/b1-f####.png 135-160 ./01-row.ntp
# NatronRenderer -b -w Write1 $renderdir/b2-f####.png 247-276 ./01-row.ntp
# NatronRenderer -b -w Write1 $renderdir/b3-f####.png 363-391 ./01-row.ntp
# NatronRenderer -b -w Write1 $renderdir/b4-f####.png 460-493 ./01-row.ntp
# NatronRenderer -b -w Write1 $renderdir/b5-f####.png 583-608 ./01-row.ntp


### MERGE EACH BAR IMAGE SEQUENCE INTO A VIDEO FILE
# ffmpeg -r 25 -f image2 -start_number 13 -i $renderdir/b0-f%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p $renderdir/bar0.mov
# ffmpeg -r 25 -f image2 -start_number 135 -i $renderdir/b1-f%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p $renderdir/_bar1.mov
# ffmpeg -r 25 -f image2 -start_number 247 -i $renderdir/b2-f%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p $renderdir/_bar2.mov
# ffmpeg -r 25 -f image2 -start_number 363 -i $renderdir/b3-f%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p $renderdir/_bar3.mov
# ffmpeg -r 25 -f image2 -start_number 460 -i $renderdir/b4-f%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p $renderdir/_bar4.mov
# ffmpeg -r 25 -f image2 -start_number 583 -i $renderdir/b5-f%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p $renderdir/_bar5.mov


### SEQUENCE ALL BAR VIDEOS INTO A SINGLE VIDEO
# NatronRenderer -b -w Write1 $renderdir/_bars.mov 1-176 ./02-row-sequencer.ntp


### RECURSION ITERATION; VERTICAL SCALE-DOWN EACH BAR TO 25% AND STACK FOUR DUPLICATES

renderdir=$outdir'/step03'
ntp='./03-row-copier.ntp'
# NatronRenderer -b -w Write1 $renderdir/03-01.mov 1-250 $ntp
# NatronRenderer -b -i Read0 $renderdir/03-01.mov -w Write1 $renderdir/03-02.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-02.mov -w Write1 $renderdir/03-03.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-03.mov -w Write1 $renderdir/03-04.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-04.mov -w Write1 $renderdir/03-05.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-05.mov -w Write1 $renderdir/03-06.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-06.mov -w Write1 $renderdir/03-07.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-07.mov -w Write1 $renderdir/03-08.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-08.mov -w Write1 $renderdir/03-09.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-09.mov -w Write1 $renderdir/03-10.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-10.mov -w Write1_h264 $renderdir/03-11.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-11.mov -w Write1_h264 $renderdir/03-12.mov 100-350 $ntp
# NatronRenderer -b -i Read0 $renderdir/03-12.mov -w Write1_h264 $renderdir/03-13.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-13.mov -w Write1_h264 $renderdir/03-14.mov 100-350 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-14.mov -w Write1_h264 $renderdir/03-15.mov 100-600 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-14.mov -w Write1_h264 $renderdir/03-15.mov 100-600 $ntp
# sleep 3
# NatronRenderer -b -i Read0 $renderdir/03-15.mov -w Write1_h264 $renderdir/03-16.mov 100-600 $ntp
# sleep 3
NatronRenderer -b -i Read0 $renderdir/03-16.mov -w Write1_h264 $renderdir/03-17.mov 100-600 $ntp
