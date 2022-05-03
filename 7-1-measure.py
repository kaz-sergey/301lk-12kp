import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt


dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
comparator = 4
troykaModul = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comparator, GPIO.IN)
#podali na troyka modul 3.3v
GPIO.setup(troykaModul, GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def num2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

def measure():
    for i in range(256):
        
        sig = num2dac(i)
        time.sleep(0.0007)
        compv = GPIO.input(comparator)
        if compv == 0:
            volt = i / levels * maxVoltage
            #print("ADC value = {:.^3} -> {}, input voltage = {:.2f}".format(i,sig,volt))

            disp = decimal2binary(i)
            GPIO.output(leds, disp)   
            break   

    return volt





try:
    dat = []
    vol = 0
    did = False
    start = time.time()
    print("Charging")
    while True:
        
        vol = measure()
        if vol < 3.3*0.97:
            tim = time.time()-start
            dat.append([int(vol/3.3*256),tim])

        if vol >= 3.3*0.97:
            #ybrali s troyka modul 3.3v
            GPIO.setup(troykaModul, GPIO.OUT, initial=GPIO.LOW)
            did = True
            print("Uncharging")
        if did and vol <= 3.3*0.02:
            end = time.time()
            length = end-start
            
            summ = 0
            for i in dat:
                summ += i[1]
            mid = summ/len(dat)

            print('length', length)
            print('mesurement time',tim)
            print('avg. discretisation time',1/mid)
            print('quant shag',3.3/258)
            d = []
            for u in dat:
                d.append(u[0])
            with open('data.txt','w') as f:
                for i in d:
                    f.write(str(i)+'\n')
            with open('sett.txt','w') as f:
                f.write('length'+ str(length)+'\n')
                f.write('mesurement time'+str(tim)+'\n')
                q = 1/mid
                z = 3.3/258
                f.write('avg. discretisation time'+str(q)+'\n')
                f.write('quant shag'+str(z)+'\n')
            
            plt.plot(d)
            plt.show()
            print("Work copmleted")
            break

            
        
except KeyboardInterrupt:
    print("The program was stoped by the keyboard")
else:
    print("No exceptions")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(leds)   
    GPIO.setup(troykaModul, GPIO.OUT, initial=GPIO.LOW)
    GPIO.cleanup(troykaModul)

    print("GPIO cleanup completed")