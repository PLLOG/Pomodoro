import winsound
import time
import csv
import os
def str_modif(strInput):
    newString=strInput.strip(',.!? ').lower()
    return newString
def timer_check_inp(timeInput):
    timeInput=str(timeInput)
    timeInput=timeInput.strip(',.!? ')
    timerTemp=timeInput.replace('.','')
    if timerTemp.isdigit():
        return timeInput
    else:
        return 0
def list_goals(fileName):
    with open(fileName,'r',encoding='utf-8',newline='') as csvfile:
        reader=csv.reader(csvfile)
        next(reader,None)
        for row in reader:
            if not row:
                print('Список пуст\n')
            else:
                print (f'В цели {row[0]}, у вас {row[1]} помидорок\n')
def list_timers(fileName):
    with open(fileName,'r',encoding='utf-8',newline='') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            match row[0]:
                case 'session':
                    print(f'Длительность сессии концетрации :{row[1]} минут\n')
                case 's_break':
                    print(f'Длительность маленького перерыва :{row[1]} минут\n')
                case 'b_break':
                    print(f'Длительность большого перерыва :{row[1]} минут\n')
                case _:
                    pass
            
def add_goal(fileName,goalName):
    with open (fileName,'a',encoding='utf-8',newline='')as csvfile:
        filewriter = csv.writer(csvfile,delimiter=',')
        filewriter.writerow([goalName,0])
def delete_goal(fileName,goalName):
    with open(fileName,'r',newline='',encoding='utf-8')as csvfile:
        reader=csv.reader(csvfile)
        list_of_goals=[]
        next(reader)
        for row in reader:
            if not row:
                print('Список пуст\n')
                return
            else:
                list_of_goals.append(row[0])
    if goalName in list_of_goals:
        temp_file = fileName +'.tmp'
        with open(fileName,'r',newline='',encoding='utf-8') as infile,\
        open (temp_file,'w',newline='',encoding='utf-8') as outfile:

            reader=csv.reader(infile)
            writer=csv.writer(outfile)

            header = next(reader)
            writer.writerow(header)
            for row in reader:
                if row[0] != goalName:
                    writer.writerow(row)

        os.replace(temp_file,fileName)
        print('Цель удалена\n')
    else:
        print('Цель не найдена\n')
def add_pom_to_goal(fileName,goalName):
    rows = []
    with open(fileName,'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader) 
        rows.append(header)
        for row in reader:
            rows.append(row)
            
    for row in rows:
        if row[0] == goalName: 
            row[1] = int(row[1])+1
            rows[0][2]=int(rows[0][2])+1
            break
    
    
    with open(fileName,'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)
    

def timer_set(fileName,timerName,newTime):
    rows = []
    with open(fileName,'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader) 
        rows.append(header)
        for row in reader:
            rows.append(row)
            
    for i, row in enumerate(rows[0:], start=0):
        if len(row) > 1 and row[0] == timerName: 
            row[1] = newTime
            break
    
    
    with open(fileName,'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)
    
def get_time(fileName,timerName):
    with open(fileName,'r',newline='',encoding='utf-8')as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            if row[0] == timerName:
                return float(row[1])
def get_total_pom(fileName):
    with open(fileName,'r',encoding='utf-8',newline='') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            return row[2]
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
    print('Сессия началась!\n')
    play_sound('sound\\clock-ticking.wav')
    while True:
        time.sleep(1)
        if time.time() >= timerFinish:
            stop_all_sound()
            play_sound('sound\\alarm.wav')
            time.sleep(3)
            stop_all_sound()
            break
    
    print ('Сессия завершена!\n')
def s_break(breakTimeInput):
    print(f'Время перерыва! Отдохните {breakTimeInput} минут\n')
    timerStart = time.time()
    breakTime=float(breakTimeInput*60)
    timerFinish=timerStart+breakTime
    while True:
        time.sleep(1)
        if time.time() >=timerFinish:
            play_sound('sound\\alarm.wav')
            time.sleep(3)
            stop_all_sound()
            print('Перерыв завершен!\n')
            break
def session_progress():
    sessionNum=0
    while True:
        sessionName=input('Введите название цели, для выхода "выход": ')
        sessionName=str_modif(sessionName)
        if sessionName == 'выход':
            break
        else:
            with open('goal_list.csv','r',encoding='utf-8',newline='')as csvfile:
                reader=csv.reader(csvfile)
                list_of_goals=[]
                next(reader,None)
                for row in reader:
                    if not row:
                        pass
                    else:
                        list_of_goals.append(row[0])
            if sessionName in list_of_goals:
                choose_to_cont=input('''
Такая цель сессии уже существует
Хотите продолжить работать над ней?(да/нет)
:''')
                choose_to_cont=str_modif(choose_to_cont)
                match choose_to_cont:
                    case 'да':
                        session(get_time('time_set.csv','session'))
                        add_pom_to_goal('goal_list.csv',sessionName)
                        sessionNum+=1
                        if sessionNum>4:
                            s_break(get_time('time_set.csv','b_break'))
                        else:
                            s_break(get_time('time_set.csv','s_break'))
                    case 'нет':
                            continue
            else:
                
                add_goal('goal_list.csv',sessionName)
                session(get_time('time_set.csv','session'))
                add_pom_to_goal('goal_list.csv',sessionName)
                sessionNum+=1
                if sessionNum>4:
                    s_break(get_time('time_set.csv','b_break'))
                else:
                    s_break(get_time('time_set.csv','s_break'))
while True:
    print(f'Вы заработали {get_total_pom("goal_list.csv")} помидорок\n')
    choice = input('''
Для начала сессии введите "старт"
Для списка целей введите "список"
Для удаления цели введите "удалить"
Для настройки таймеров введите "настройка"
Для выхода введите "выход"
    :''')
    choice = str_modif(choice)
    match choice:
        case 'старт':
            session_progress()
        case 'список':
            list_goals('goal_list.csv')
        case 'удалить':
            list_goals('goal_list.csv')
            choose_to_del=input('Введите цель для удаления: ')
            choose_to_del=str_modif(choose_to_del)
            delete_goal('goal_list.csv',choose_to_del)
            
        case 'настройка':
            list_timers('time_set.csv')
            choose_time_to_cg=input(f'''
Введите название таймера для изменения
(большой/маленький/сессия):''')
            choose_time_to_cg=str_modif(choose_time_to_cg)
            match choose_time_to_cg:
                case 'большой':
                    while True:
                        time_inp=input('Введите новое время в минутах:')
                        if timer_check_inp(time_inp) == '0':
                            print('Неверный ввод\n')
                            continue
                        timer_set('time_set.csv','b_break',time_inp)
                        break
                case 'маленький':
                    while True:
                        time_inp=input('Введите новое время в минутах:')
                        if timer_check_inp(time_inp) == '0':
                                print('Неверный ввод\n')
                                continue
                        timer_set('time_set.csv','s_break',time_inp)
                        break
                case 'сессия':
                    while True:
                        time_inp=input('Введите новое время в минутах:')
                        if timer_check_inp(time_inp) == '0':
                                print('Неверный ввод\n')
                                continue
                        timer_set('time_set.csv','session',time_inp)
                        break
                case _:
                    print('Неверное имя таймера\n')
            
        case 'выход':
            break

        case _:
            print ('нераспознанная команда\n')


def test(): # Код для PR
    pass
            
                            
                
            












            
