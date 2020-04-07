import simpleaudio as sa
import wave
import time
import glob
import os 
import threading
import random
from random import randint
import argparse
import math
import ast
import pygame
import numpy

global l_1, l_2, llx , dlx, b, deg, tick, notehash, num, tempo, count, counter, rn_t, rn
global bassline, ground, third, fifth, octave, hll1, hll2, hll3, hll4, hll5, hll6, dll1, dll2, dll3, dll4, dll5, dll6
global xll1, xll2, xll3, xll4, xll5, xll6, c1, ill, chordlist, basshash
global b_1, b_2, b_3, b_4, b_5, b_6, b_d

#setting the tick event, that synchronizes all events

tick = threading.Event()
listchange = threading.Event()
firstbeat = threading.Event()

running = False

#the next variable is the one that counts it's way through the melody lists.
c1 = 0

#just using an example of possible lists here:
l_1 = 0
l_2 = 0

counter = 0 #counter is the variable that counts the total length of the playback.

#defining variables for root note selection

r = randint(48,57) #root note
rn = r - 48 #root note conversion
rn_t = rn
j = 0

# declaring home directory for loading in the home folder

dir_path = os.path.dirname(os.path.realpath(__file__))

#init of all lists, dicts and ints

sc = []
names = []
reg = {}
notehash = {}

num = 0 # this on ensures the seg count remains accurate
beat = 0
bar = 0
seg = -1
dur = [4,4,4,4]
tl = len(dur)

#the next flag is used to check whether the bass line is still to play.
bass_is_done = False

#How to work out a changing rhythm

tempo = 350.0
b = 60.0/tempo #b is the duration of 1 beat. 

# defining the bass variables

ground = None
third = None
fifth = None
octave = None

basshash = {
    'ground' : ground,
    'third' : third,
    'fifth' : fifth,
    'octave' : octave
}


#This works as a basic mechanism to load a sample

sc = ['g48','g49','g50','g51','g52','g53','g54','g55','g56','g57','g58','g59','g60','g61','g62','g63','g64','g65','g66','g67','g68','g69','g70','g71','g72','g73','g74','g75','g76','g77','g78','g79','g80','g81','g82','g83','g84','g85','g86','g87','g88','g89','g90','g91','g92','g93','g94','g95','g96']
names = glob.glob(dir_path + "/S/*.wav")
names = sorted(names)

#declaring format functions here

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def lsflatten(x):
    x = ast.literal_eval(x)
    x = x[0]
    return x

def lsformat(notelist, durlist):
    #this function changes combines the duration list and note list into a flat list, that uses the strin 'r' for a rest not
    y = 0
    fullist = []

    while y < len(notelist):
        fullist.append(notelist[y])
        for i in range (durlist[y]-1):
            fullist.append('r')
        y += 1

    return fullist

def chformat(degree,segment):
    #this function creates a list that has the same format as the notelists, only using the chord degrees on the appropriate spot
    y = 0
    fullist = []

    while y < len(degree):
        for x in range(segment[y]):
            fullist.append(degree[y])
        y+=1

    fullist.extend(fullist)
    
    return fullist

    # loading some example lists

hll1 = [2,1,3,3,2,1,1,1,2,1,3,3,2,1,4,99]
dll1 = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]

xll1 = lsformat(hll1,dll1)

hll2 = [2,1,1,3,3,2,1,1,1,1,2,4,1,3,3,2,3,1,4,99]
dll2 = [4,4,8,8,8,4,4,8,8,8,4,4,8,8,8,4,4,8,8,8]

xll2 = lsformat(hll2,dll2)

hll3 = [2,1,1,3,4,3,2,1,1,1,2,1,2,4,1,3,4,3,2,3,1,4,6,99]
dll3 = [4,4,8,4,4,8,4,4,8,4,4,8,4,4,8,4,4,8,4,4,8,8,4,4]

xll3 = lsformat(hll3,dll3)

hll4 = [2,1,1,2,3,4,3,2,1,1,2,1,2,1,2,4,1,2,3,4,3,2,3,1,3,4,6,99]
dll4 = [4,4,4,4,4,4,8,4,4,4,4,4,4,8,4,4,4,4,4,4,8,4,4,4,4,8,4,4]

xll4 = lsformat(hll4,dll4)


hll5 = [2,1,1,'2a',2,3,4,3,'3b',2,1,1,'2a',2,1,2,1,'1a',2,4,1,'2a',2,3,4,3,2,2,3,'99a',2,0,1,3,4,6,99]
dll5 = [4,4,2,2,4,4,4,4,4,4,4,2,2,4,4,4,4,4,4,4,2,2,4,4,4,4,4,4,1,1,1,1,4,4,8,4,4]

xll5 = lsformat(hll5,dll5)

hll6 = [2,'1b',1,1,'2a',2,4,3,4,3,'3b',2,'2b',1,1,'2a',2,'2b',1,2,1,'1a',2,'99a',3,'3a',4,1,'2a',2,3,3,4,3,2,2,3,'99a',2,0,1,3,2,4,6,99]
dll6 = [2,2,4,2,2,2,2,4,4,4,4,2,2,4,2,2,2,2,4,4,4,4,1,1,1,1,4,2,2,2,2,4,4,4,4,4,1,1,1,1,4,2,2,8,4,4]                  
            
xll6 = lsformat(hll6,dll6)

deg = [0, 3, 4, 4]
dur = [4, 4, 4, 4]
chordlist = chformat(deg,dur)

b_d = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]

b_1 = ['ground','third','fifth','ground','ground','fifth','third','fifth','fifth','ground','third','ground','ground','third','fifth','third','fifth','ground','third','ground','ground','fifth','third','fifth','fifth','ground','third','ground','ground','third','fifth','ground']
xb_1 = lsformat(b_1, b_d)
            
b_2 = ['fifth','ground','third','ground','ground','third','fifth','third','ground','third','fifth','third','ground','fifth','third','fifth','ground','fifth','third','fifth','ground','third','fifth','third','fifth','ground','third','ground','ground','third','fifth','third']
xb_2 = lsformat(b_2, b_d)

b_3 = ['ground','third','fifth','third','ground','fifth','third','fifth','ground','third','fifth','ground','ground','third','fifth','third','fifth','ground','third','ground','ground','third','fifth','third','ground','third','fifth','ground','ground','third','fifth','third']
xb_3 = lsformat(b_3, b_d)

b_4 = ['ground','third','fifth','ground','fifth','ground','third','ground','ground','fifth','third','fifth','ground','fifth','third','fifth','ground','fifth','third','fifth','ground','fifth','third','fifth','ground','fifth','third','fifth','ground','fifth','third','fifth']
xb_4 = lsformat(b_4, b_d)

b_5 = ['fifth','ground','third','ground','ground','fifth','third','fifth','ground','fifth','third','fifth','ground','third','fifth','third','fifth','ground','third','ground','ground','fifth','third','fifth','ground','third','fifth','third','ground','third','fifth','third']
xb_5 = lsformat(b_5, b_d)

b_6 = ['fifth','ground','third','ground','ground','third','fifth','third','fifth','ground','third','ground','ground','fifth','third','fifth','ground','fifth','third','fifth','ground','third','fifth','third','ground','third','fifth','ground','ground','fifth','third','fifth']
xb_6 = lsformat(b_6, b_d)

bassline = xb_6

llx = xll6
dlx = xll6
            
# the next list contains the main list sliced in 4
ill = llx[::4]

count = len(llx)


#declaring all the functions here

def killswitch():
    global running
    
    print ("killswitch engaged")
    while (not running):
        pass

def reader(n):
    obj = pygame.mixer.Sound(n)
    return obj

def scalemaker(i):
    global Maj

    Maj = [i,i+2,i+4,i+5,i+7,i+9,i+11,i+12,i+14,i+16,i+17,i+19,i+21,i+23,i+24,i+26,i+28,i+29,i+31,i+33,i+35,i+36]
    
    notehashr = {
        0: reg[sc[Maj[9]]],
        1: reg[sc[Maj[11]]],
        2: reg[sc[Maj[14]]],
        3: reg[sc[Maj[16]]],
        4: reg[sc[Maj[18]]],
        5: reg[sc[Maj[21]]],
        '0b': reg[sc[Maj[8]]],
        '1b': reg[sc[Maj[10]]],
        '2b': reg[sc[Maj[13]]],
        '3b': reg[sc[Maj[15]]],
        '4b': reg[sc[Maj[17]]],
        '5b': reg[sc[Maj[20]]],
        '0a': reg[sc[Maj[10]]],
        '1a': reg[sc[Maj[12]]],
        '2a': reg[sc[Maj[15]]],
        '3a': reg[sc[Maj[17]]],
        '4a': reg[sc[Maj[19]]],
        '5a': reg[sc[Maj[21]]]
    }
    return notehashr

def changer(chg=0):
    global deg, seg, Maj, tl, ground, third, fifth, octave, num, bassline, llx, ill, chordlist, basshash
    
    #the function assigns notes to the variables.

    if num == 0:
        num += 1
    else:
        if seg + chg == tl:
            seg = -1
        else:
            pass

    ground = reg[sc[Maj[deg[seg+chg]]]]
    third = reg[sc[Maj[deg[seg+chg]+2]]]
    fifth = reg[sc[Maj[deg[seg+chg]+4]]]
    octave = reg[sc[Maj[deg[seg+chg]+7]]]

    basshash = {
        'ground' : ground,
        'third' : third,
        'fifth' : fifth,
        'octave' : octave
    }

# Declaring the loops that will be running threaded

def thecount():
    global beat, bar, seg, dur, b, running, counter
    while True:
        tick.wait()
        if beat > 3:
            if bar == dur[seg]:
                bar = 1
                seg += 1
                if seg == tl:
                    seg = -1
                else:
                    pass
                firstbeat.set()
                firstbeat.clear()

            else:
                bar += 1
                beat = 0
                counter += 1

        else:
            beat += 1         

def metronome():
    global b
    while True:
        tick.set()
        tick.clear()
        time.sleep(b)

def melody():
    #declaring variables before the loop
    global llx, dlx, notehash, b, running, count, c1

    n1 = 0
    sx = 0

    #waiting for the firstbeat
    #starting the loop
    while True:
        firstbeat.wait()
        while True:
            if llx[c1] == 'r':
                pass
            else:
                try:
                    notehash[llx[c1]].play()
                except KeyError:
                    pass

            c1 += 1
            
            if c1 == count:
                break

            #counting the amount of ticks necesarry.
            #for _ in range(dlx[c1-1]):
            #    tick.wait()

            time.sleep(0.05)
            tick.wait()

        c1 = 0
        listchange.set()
        listchange.clear()

        if sx == 0:
            sx = 1
        else:
            sx = 0

def bass():
    global b, ground, third, fifth, octave, running, bassline, basshash
    
    basslength = len(bassline)
    #waiting for the first loop
    firstbeat.wait()
    while True:
        for x in range(basslength):
            if bassline[x] == 'r':
                if x == 15:
                    changer(1)

                else:
                    pass
            else:
                basshash[bassline[x]].play()

            tick.wait()

def tempocontrol():
    global b, vol1, avg_1, tempo, running
    while True:
        tick.wait()
        #the line below defines the sensitivity of the slowing of the tune
        d = ( tempo / 1000.0 )

        """
        if vol1 > avg_1:
            tempo = tempo + d - 0.05
        elif vol1 <= avg_1:
            tempo = tempo - d - 0.05
        """

        #The next line should be uncommented if the rhythm is to change
        #b = 60.0/tempo

def keychange():
    global rn_t, rn, notehash
    if rn_t == rn:
        if rn >= 7:
            rn_t = rn - random.choice([5,8,0,0,0])
            notehash = scalemaker(rn_t)
        else:
            rn_t = rn + random.choice([4,7,0,0,0])
            notehash = scalemaker(rn_t)
    else:
        rn_t = rn
        notehash = scalemaker(rn)

def listchanger():
    global count, l_1, l_2, llx, dlx, hll1, hll2, hll3, hll4, hll5, hll6, dll1, dll2, dll3, dll4, dll5, dll6

    while True:
        listchange.wait()
        if tempo > 260:
            l_2 = 1
            llx = xll5
            dlx = dll5
            bassline = xb_5
            count = len(llx)
        elif tempo <= 260 and tempo > 230:
            l_2 = 2
            llx = xll4
            dlx = dll4
            bassline = xb_4
            count = len(llx)
        elif tempo <= 230 and tempo > 210:
            l_2 = 3
            llx = xll3
            dlx = dll3
            bassline = xb_3
            count = len(llx)
        elif tempo <= 210 and tempo > 195:
            l_2 = 4
            llx = xll2
            dlx = dll2
            bassline = xb_2
            count = len(llx)
        elif tempo <= 195 and tempo > 185:
            l_2 = 5
            llx = xll1
            dlx = dll1
            bassline = xb_1
            count = len(llx)
        elif tempo <= 185:
            print ('we got there')
            llx = [99,99,99,99]
            bass_is_done = True
            count = counter

        if l_1 == l_2:
            keychange()
            changer()
        else:
            pass

        l_1 = l_2


#initializing the mixer from pygame. the pre-init loads a smaller buffer than default to improve audio latency.
#Setting more channels hopefully allows more accurate playback
pygame.mixer.pre_init(44100,-16,2, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(32)

# converting all the links into playable simpleaudio object, callable through .play()

names = [ reader(x) for x in names ]

# building the register, that contains all the notes.

reg = {}

for i in range(len(sc)):
    reg[sc[i]] = names[i]

#the way to play a note now, is 'reg["g80"].play()'


def main():
    global running, notehash, hllx, dlx, hll1, hll2, hll3, hll4, hll5, hll6, dll1, dll2, dll3, dll4, dll5, dll6, deg_x, seg_x
    
    notehash = scalemaker(rn)
    changer()

    #adding daemon = True, means it runs as a slave to the main thread, which I will make Killswitch

    t1 = threading.Thread(target = metronome)
    t1.daemon = True

    t2 = threading.Thread(target = melody)
    t2.daemon = True

    t3 = threading.Thread(target = bass)
    t3.daemon = True

    t5 = threading.Thread(target = tempocontrol)
    t5.daemon = True

    t6 = threading.Thread(target = listchanger)
    t6.daemon = True

    t7 = threading.Thread(target = thecount)
    t7.daemon = True

    t0 = threading.Thread(target = killswitch)

    #Below all the processes are started

    t0.start()
    t1.start()
    t7.start()
    t2.start()
    t3.start()
    t5.start()
    t6.start()
    
    input("Enter to quit")

    running = True
    #line below attempts to shut down the osc server
    
if( __name__ == "__main__"):

    main()


