import subprocess
#from moviepy.editor import VideoFileClip
#import librosa

type = "audio"
file = "output.txt"

if type == "video":
    print(subprocess.Popen("ffmpeg -f concat -safe 0 -i " + str(file) + " -c copy ./output/output_video.mp4", shell=True).wait())

elif type == "audio":
    print(subprocess.Popen("ffmpeg -f concat -safe 0 -i " + str(file) + " -c copy ./output/output_video.aac", shell=True).wait())

else:
    print("./output/output_image.png")
