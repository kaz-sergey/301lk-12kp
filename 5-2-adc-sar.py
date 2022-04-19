import RPi.GPIO as GPIO
import time
dac=[26,19,13,6,5,11,9,10]
bits=len(dac)
levels=2**bits
maxVoltage=3.3
troykaModule=17
comparator=4

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(troykaModule, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]
def num2dac(value):
    signal=decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

try:
    while True:
        value=128
        left=0
        right=255
        while True:
            signal=num2dac(value)
            voltage=value/levels*maxVoltage
            time.sleep(0.00125)
            comparatorValue=GPIO.input(comparator)
            if comparatorValue==0:
                right=value-1
                value=(left+right)//2
            else:
                left=value+1
                value=(left+right)//2
            if right<left:
                print("ADC value = {:^3} -> {}, input voltage = {:.2f}".format(value, signal, voltage))
                break
except KeyboardInterrupt:
    print('\nThe program was stopped by the keyboard')
else:
    print("No exceptions")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print('GPIO cleanup completed')