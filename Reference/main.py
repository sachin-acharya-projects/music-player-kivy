import tkinter as tk
from tkinter import filedialog
from vlc import MediaPlayer
import os, time, json, requests
from pytube import YouTube
from pytube.cli import on_progress

username = os.path.dirname(__file__)

# CREATING FILEDIALOGUE
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)

def musicFile():
    return list(filedialog.askopenfilenames())
def rename(cb):
    print("Results: ", cb)
def getMedia(topic):
    url = 'https://www.youtube.com/results?q=' + topic
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count+=1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count-5] == "/results":
        raise Exception("No Video Found with that name")
    return "https://www.youtube.com"+lst[count-5]

itter = ''
options = [
    ('Play', 'Play Music/Unpause Music'),
    ('Pause', 'Pause Music'),
    ('Stop', 'Stop Music'),
    ('Quit / exit', 'Close Player'),
    ('Status', 'Show Current Status of Music'),
    ('Volume', 'Set Volume Level'),
    ('mute/unmute', 'Mute/Unmute Audio'),
    ('Change', 'Change Current music'),
    ('set time', 'Set Current Time'),
    ('Clear', 'Clear Screen'),
    ('Next', 'Change to Next Song'),
    ('prev', 'Change to Previous Song'),
    ('ls', 'View List of Song'),
    ('update repo', 'Update to GitHub'),
    ('add', 'Add More Files')
]
constant = 0
if __name__ == '__main__':
    while True:
        print("""Menus
        1. Choose Local Media
        2. Search from YouTube
        """)
        menu = input(': ')
        data = ''
        musicName = ''
        isLocal = False
        if menu.isdigit():
            if int(menu) == 1:
                musicName = str(musicFile()[constant])
                data = MediaPlayer(musicName)
                isLocal = True
            elif int(menu) == 2:
                musicName = input("Enter Music Title: ")
                videoUrl = str(getMedia(musicName))
                musicName = videoUrl
                data = MediaPlayer(YouTube(videoUrl).streams.get_audio_only().url)
                isLocal = False
            else:
                print("InValid Option passed")
                print("Exiting Program...")
                exit(0)
        else:
            print("InValid Option passed")
            print("Exiting Program...")
            exit(0)
        while True:
            if itter == 'play':
                ask = 'play'
                itter = ''
            else:
                ask = input('user@root:~ ').lower()
            if ask == 'play':
                if str(data.get_state()).split('.')[1] == 'Ended':
                    musicFile = list(filedialog.askopenfilenames())
                    itter = 'play'
                    data.stop()
                    break
                else:
                    print('Playing Audio')
                    data.play()
                    time.sleep(1)
            elif ask == 'save':
                with open(os.path.join(username, 'Data\\playlist.json'), 'r+') as file:
                    if len(file.readlines()) == 0:
                        Contentdata = {
                            "list": [musicName]
                        }
                    else:
                        lst = json.loads(file)
                        # Contentdata = list(json.load(file)['list'])
                        print("List", lst)
                        Contentdata.push(musicName)

                        Contentdata = {
                            "list": Contentdata
                        }
                    file.seek(0)
                    file.truncate()
                    json.dump(Contentdata, file, indent=4)
                    print("Music has been saved")
            elif ask == 'download':
                if(isLocal):
                    print("Media File is Locally available so cannot download which is already exist")
                else:
                    print("Downloading Media File")
                    url = getMedia(musicName)
                    ytd = YouTube(url, on_progress_callback=on_progress)
                    asking = input("""Choose Options
                    (A)udio
                    (V)ideo
                    """).lower()
                    if asking == 'a':
                        title = ytd.title
                        print("Downloading Audio {}.mp3".format(title))
                        try:
                            cb = ytd.streams.get_audio_only().download(f"{username}\Musics")
                        except ConnectionResetError:
                            print("Audio cannot be downloaded=> Connection has been reset")
                        ytd.register_on_complete_callback(rename(cb))
                    elif asking == 'v':
                        print("Downloading Video {}.mp4".format(ytd.title))
                        try:
                            ytd.streams.get_highest_resolution().download(f"{username}\Videos")
                        except:
                            print("Video cannot be downloaded=>Connection reset")
                    else:
                        print("Invalid Argument")
                    print("Download is Completed Successful")
            elif ask == 'pause':
                print('Pausing Audio')
                time.sleep(0.5)
                data.pause()
            elif ask == 'next':
                constant = len(musicFile)-1 if (constant+1) >= len(musicFile) else constant+1
                print('No More Files are there!Play Last File' if (constant+1) >= len(musicFile) else constant+1)
                itter = 'play'
                data.stop()
                break
            elif ask == 'prev':
                constant = constant - 1
                itter = 'play'
                data.stop()
                break
            elif ask == 'choose':
                innerAsk = input('Enter Number (ls for list): ').lower()
                if innerAsk == 'ls':
                    cnt = 0
                    for item in musicFile:
                        print('0'+str(cnt) if cnt < 10 else cnt, ') ', str(item).split('/')[-1])
                        cnt += 1
                    innerAsk = input('Enter Number: ')
                else:
                    innerAsk = int(innerAsk)
                if innerAsk == 'exit':
                    print('Exiting Music Player')
                    time.sleep(1)
                    exit()
                else:
                    try:
                        constant = int(innerAsk)
                    except Exception:
                        pass
                itter = 'play'
                data.stop()
                break
            elif ask == 'stop':
                print('Stopping Audio')
                time.sleep(0.5)
                data.stop()
            elif ask == 'quit' or ask == 'exit':
                print('Exiting Music Player')
                time.sleep(1)
                exit()
            elif ask == 'clear' or ask == 'cls':
                print('Clearing Screen')
                time.sleep(0.5)
                os.system('cls')
            elif ask == 'change':
                musicFile = filedialog.askopenfilenames()
                itter = 'play'
                data.stop()
                break
            elif ask == 'mute':
                if data.audio_get_mute() == 0:
                    print('Muting Audio')
                    time.sleep(0.5)
                    data.audio_toggle_mute()
                else:
                    print('Already Muted\nCurrent Volume Level: {}'.format(data.audio_get_volume()))
            elif ask == 'unmute':
                if data.audio_get_mute() == 1:
                    print('Unmuting Audio')
                    time.sleep(0.5)
                    data.audio_toggle_mute()
                else:
                    print('Already Unmuted\nCurrent Volue Level: {}'.format(data.audio_get_volume()))
            elif ask == 'status':
                print('Status-------------------------------------')
                print('State: {}'.format(str(data.get_state()).split('.')[1]))
                if data.audio_get_mute() == 0:
                    print('Muted/Unmuted: Unmuted')
                else:
                    print('Muted/Unmuted: muted')
                print('Length(MS): {}'.format(data.get_length()))
                print('Current Length: {}'.format(data.get_time()))
                print('Volume Level: {}'.format(data.audio_get_volume()))
            elif ask == 'volume':
                print('Current Level: {}'.format(data.audio_get_volume()))
                level = input('New Level (0 - 100): ')
                if level == '':
                    pass
                else:
                    data.audio_set_volume(int(level))
            elif ask == 'set time':
                tm = int(input('Enter Time (0 - {}): '.format(data.get_length())))
                data.pause()
                data.set_time(tm)
                data.play()
            elif ask == 'options' or ask == 'opt':
                print('Options',' '*(15-len('Options')), ':','Functions')
                print('\n')
                for item in options:
                    print(item[0],' '*(15-len(item[0])),':',item[1])
            elif ask == 'test':
                print(data.get_time())
                data.set_time(3400)
            elif ask == 'update repo':
                os.system('git pull&&git push')
            elif ask == 'add':
                getItem = list(filedialog.askopenfilenames())
                musicFile.append(getItem)
                time.sleep(0.2)
                print('{} Files added to Current List'.format(len(getItem)))
            elif ask == 'ls':
                cnt = 0
                for item in musicFile:
                    print('0'+str(cnt) if cnt < 10 else cnt, ') ', str(item).split('/')[-1])
                    cnt += 1
            else:
                print(data.is_playing())