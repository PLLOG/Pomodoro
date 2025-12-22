import winsound
import time
import csv
def add_goal(goalName,pomodoroNum):
    with open (filename,'a',encoding='utf-8',newline='')as csvfile:
        filewiter = csv.writer(csvfile,delimeter=',')
        
def play_sound(name):
    WAV_FILE = name
    PLAY_FLAGS = winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC
    winsound.PlaySound(WAV_FILE, PLAY_FLAGS)
def stop_all_sound():
    winsound.PlaySound(None,winsound.SND_PURGE)
def session(name,sessionTimeInput):
    timerStart=time.time()
    sessionTimeSec=float(sessionTimeInput*60)
    timerFinish=timerStart+sessionTimeSec
    play_sound('sound\\clock-ticking.wav')
    while True:
        time.sleep(1)
        if time.time() >= timerFinish:
            stop_all_sound()
            play_sound('sound\\alarm.wav')
            time.sleep(3)
            stop_all_sound()
            break
    
    print ('done')
def s_break():
    pass
pass
