import winsound
import time
import csv
import os
def add_goal(fileName,goalName,pomNum):
    with open (fileName,'a',encoding='utf-8',newline='')as csvfile:
        filewriter = csv.writer(csvfile,delimiter=',')
        filewriter.writerow([goalName,0,pomNum])
def delete_goal(fileName,goalName,column_name=0):
    temp_file = fileName +'.tmp'
    with open(fileName,'r',newline='',encoding='utf-8') as infile,\
    open (temp_file,'w',newline='',encoding='utf-8') as outfile:

        reader=csv.reader(infile)
        writer=csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        try:
            column_index = header.index(column_name)
        except ValueError:
            print(f'Error: Column {column_name} not found.')
            return

        for row in reader:
            if row[column_index] != goalName:
                writer.writerow(row)

    os.replace(temp_file,fileName)
    print('deleted')
def add_pom_to_goal(fileName,goalName):
    rows = []
    with open(fileName, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader) 
        rows.append(header)
        for row in reader:
            rows.append(row)
            
    for i, row in enumerate(rows[0:], start=0):
        if len(row) > 1 and row[0] == goalName: 
            row[1] = int(row[1])+1
            rows[0][3]=int(rows[0][3])+1
            break
    
    
    with open(fileName, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)
    print(f"File '{fileName}' has been updated.")
def play_sound(name):
    WAV_FILE = name
    PLAY_FLAGS = winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC
    winsound.PlaySound(WAV_FILE, PLAY_FLAGS)
def stop_all_sound():
    winsound.PlaySound(None,winsound.SND_PURGE)
def session(sessionTimeInput):
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
def s_break(breakTimeInput):
    timerStart = time.time()
    breakTime=float(breakTimeInput*60)
    timerFinish=timerStart+breakTime
    while True:
        time.sleep(1)
        if time.time() >=timerFinish:
            play_sound('sound\\alarm.wav')
            time.sleep(3)
            stop_all_sound()
            break
        

