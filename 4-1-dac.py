import RPi.GPIO as GPIO
dac=[26,19,13,6,5,11,9,10]
def decimal2binary(value):
    return [int(e) for e in bin(value)[2:].zfill(8)]
print (decimal2binary(24))
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
def isfloat(value):
    try:
        try:
            int(value)
        except ValueError:
            float(value)
            return True
        return False
    except ValueError:
        return False
try:
    while True:
        print("Введите число")
        value=input()
        if value=="q":
            break
        if ord(value[-1])<ord('0') or ord(value[-1])>ord('9'):
            print("Не число")
        
        elif isfloat(value):
            print("Нецелое число")
        
        elif int(value)<0:
            print("Отрицательное число")
        
        elif int(value)>255:
            print("Большое число")
        
        else:
            GPIO.output(dac, decimal2binary(int(value)))
            print("Voltage:",3.3/256*int(value))
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()
