import RPi.GPIO as GPIO
from time import time, sleep
a=100
fr=50
out_pin=23
GPIO.setmode(GPIO.BCM)
GPIO.setup(out_pin, GPIO.OUT)
try:
    start=time()
    p = GPIO.PWM(out_pin, fr)
    p.start(a)
    while True:
        p.ChangeDutyCycle(int(input()))


finally:
    GPIO.output(out_pin, 0)
    GPIO.cleanup()


