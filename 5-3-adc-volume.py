import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

def decimal2binary(value):
    return [int(e) for e in bin(value)[2:].zfill(8)]

def num2dac(value):
    signal=decimal2binary(value)
    GPIO.output(dac,signal)
    return signal

def light(x):
    if x<28:
        return [0,0,0,0,0,0,0,0]
    if x>=28 and x<57:
        return [0,0,0,0,0,0,0,1]
    if x>=57 and x<85:
        return [0,0,0,0,0,0,1,1]
    if x>=85 and x<114:
        return [0,0,0,0,0,1,1,1]
    if x>=114 and x<142:
        return [0,0,0,0,1,1,1,1]
    if x>=142 and x<171:
        return [0,0,0,1,1,1,1,1]
    if x>=171 and x<199:
        return [0,0,1,1,1,1,1,1]
    if x>=199 and x<228:
        return [0,1,1,1,1,1,1,1]
    if x>=228 and x<256:
        return [1,1,1,1,1,1,1,1]


GPIO.setmode(GPIO.BCM)
leds=[21,20,16,12,7,8,25,24]
dac=[26,19,13,6,5,11,9,10]
comp=4
troyka=17
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka,GPIO.OUT,initial=1)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds,GPIO.OUT)
data=[]
try:
    t_start=time.time()
    while True:
        value=128
        left=0
        right=255
        while True:
            signal=num2dac(value)
            voltage=(value)/(2**8)*3.3
            time.sleep(0.005)
            c=GPIO.input(comp)
            if c==0:
                right=value-1
                value=(left+right)//2
            else:
                left=value+1
                value=(left+right)//2
            if right<left:
                GPIO.output(leds,light(value))
                voltage=(value)/(2**8)*3.3
                if voltage<0:
                    voltage=0
                    value=0
                data.append(value)
                break
        if value>=243:
            break
    GPIO.output(troyka,0)
    while True:
        value=128
        left=0
        right=255
        while True:
            signal=num2dac(value)
            voltage=(value)/(2**8)*3.3
            time.sleep(0.005)
            c=GPIO.input(comp)
            if c==0:
                right=value-1
                value=(left+right)//2
            else:
                left=value+1
                value=(left+right)//2
            if right<left:
                GPIO.output(leds,light(value))
                voltage=(value)/(2**8)*3.3
                if voltage<0:
                    voltage=0
                    value=0
                data.append(value)
                break
        if value<=6:
            t_end=time.time()
            break
    duration=t_end-t_start
    plt.plot(data)
    plt.show()
   # data_str=[str(item) for item in data]
    #with open("data.txt", "w") as outfile:
      #  outfile.write("\n".join(data_str))
finally:
    GPIO.output(dac,0)
    GPIO.output(leds,0)
    GPIO.cleanup(dac)