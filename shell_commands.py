import subprocess
#from moviepy.editor import VideoFileClip
#import librosa

type = "audio"

if type == "video":
    start = 0
    filename = "test3.avi"
    #clip = VideoFileClip(filename)
    video_time = 227
    num = 0
    while start <= video_time - 5:
        print(subprocess.Popen("ffmpeg -ss " + str(start) + " -i " + str(filename) + " -t 5 ./output/video" + str(num) + ".mp4", shell=True).wait())
        start = start + 5
        num = num + 1

    print(subprocess.Popen("ffmpeg -ss " + str(start) + " -i " + str(filename) + " -t " + str(video_time - start) + " ./output/video" + str(num) + ".mp4", shell=True).wait())


elif type == "audio":
    start = 0
    filename = "test4.mp3"
#    audio_time = librosa.get_duration(filename)
    audio_time = 215
    num = 0
    while start <= audio_time - 20:
        print(subprocess.Popen("ffmpeg -ss " + str(start) + " -i " + str(filename) + " -t 20 ./output/audio" + str(num) + ".aac", shell=True).wait())
        start = start + 20
        num = num + 1

    print(subprocess.Popen("ffmpeg -ss " + str(start) + " -i " + str(filename) + " -t " + str(audio_time - start) + " ./output/audio" + str(num) + ".aac", shell=True).wait())


else:
    filename = "test5.jpg"
    print(subprocess.Popen("ffmpeg -i " + filename + " ./output/image.png", shell=True).wait())
