import RPi.GPIO as GPIO
import time


def dec2bin(number):
    return [int(bit) for bit in bin(number)[2:].zfill(8)]


def adc():
    for b in range(256):
        signal = dec2bin(b)
        if GPIO.input(comp) == 0:
            print(f"Current voltage -> {round(b * 3.24 / 256, 3)}")
            GPIO.output(dac, 0)
            break
        else:
            GPIO.output(dac, signal)
            time.sleep(0.0005)


dac = [10, 9, 11, 5, 6, 13, 19, 26][::-1]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp, GPIO.IN)


try:
    while True:
        adc()
        time.sleep(0.01)
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()