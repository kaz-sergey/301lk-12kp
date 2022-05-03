import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import numpy as np

# Преобразование числа из n_10 в n_2 с.с.
def decimal_to_binary(number):
    return [int(bit) for bit in bin(number)[2:].zfill(8)]


# Вывод информации на светодиоды leds (0% - 0 светодиодов, 100% - 8 светодиодов, линейно)
def led_indicator(percent):
    v = percent / 100 * 8
    volume = [int(i < v) for i in range(8)]

    GPIO.output(leds, volume)


# Вкл/выкл напряжение на тройка-модуле (on - вкл, off - выкл)
def troyka_reg(cond):
    if cond == 'on':
        GPIO.output(troyka, 1)
    elif cond == 'off':
        GPIO.output(troyka, 0)


# Аналогово-цифровой преобразователь, возвращает текущее напряжение на выходе тройка-модуля
def analog_to_digital_conventer():
    signal = decimal_to_binary(0)

    for i in range(8):

        signal[i] = 1
        GPIO.output(dac, signal)
        time.sleep(0.0005)

        if GPIO.input(comp) == 0:
            signal[i] = 0
    
    b = ''.join(map(str, signal))
    current_voltage = round((int(b, 2)), 3)

    print(f"Current number -> {current_voltage}")

    GPIO.output(dac, 0)

    return current_voltage

# Инициализирует режим работы с gpio и настраивает пины на вход/выход 
def gpio_init(input_pins, output_pins):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pins, GPIO.IN)
    GPIO.setup(output_pins, GPIO.OUT)


# Позволяет корректно завершить работу с gpio
def gpio_close(output_pins):
    GPIO.output(output_pins, 0)
    GPIO.cleanup()


if __name__ == "__main__":
    # Пины, с которыми мы будем работать
    dac = [10, 9, 11, 5, 6, 13, 19, 26][::-1]
    leds = [21, 20, 16, 12, 7, 8, 25, 24][::-1]
    comp = 4
    troyka = 17

    inp_pins = [comp]
    out_pins = dac + leds + [troyka]

    # Инициализация пинов
    gpio_init(inp_pins, out_pins)

    # Основной блок программы
    try:
        # Необходимые для работы переменные
        data = {
            'voltage': [],
            'time': []
        }
        start_time = time.time()

        # Подаём на тройка-модуль сигнал 1 (3.3В)
        troyka_reg('on')

        # Вычисляем напряжение на конденсаторе
        capacitor_charge = analog_to_digital_conventer()

        # Конденсатор заряжается
        while capacitor_charge < 245:
            cur_voltage = analog_to_digital_conventer()
            cur_time = time.time() - start_time
            data['voltage'].append(cur_voltage)
            #data['time'].append(cur_time)

            capacitor_charge = cur_voltage
            led_indicator(capacitor_charge * 3.3 / 256 * 100)
            time.sleep(0.01)
        
        troyka_reg('off')
        t_zar=cur_time
        
        # Конденсатор разряжается
        while capacitor_charge > 3:
            cur_voltage = analog_to_digital_conventer()
            cur_time = time.time() - start_time
            data['voltage'].append(cur_voltage)
            #data['time'].append(cur_time)

            capacitor_charge = cur_voltage / 3.3
            led_indicator(capacitor_charge*3.3 / 256 * 100)
            time.sleep(0.01)
        t_razr = cur_time-t_zar
        all_time = cur_time
        
        print(f'\nВремя зарядки конденсатора: {t_zar:.2f} секунд.')
        print(f'\nВремя разрядки конденсатора: {t_razr:.2f} секунд.')
        print(f'\nОбщая продолжительность эксперимента составила: {all_time:.2f} секунд.')

        # Построения графика зависимости напряжения на обкладках конденсатора от времени
       # Построения графика зависимости напряжения на обкладках конденсатора от времени
        plt.plot(data['voltage'])
       # plt.xlabel('t, с')
       # plt.ylabel('U, В')
        #plt.title('Зависимость напряжения на обкладках конденсатора U от времени t')
        plt.show()
  
        # Вычисление некоторых параметров эксперимента
        count_of_measurements = len(data)
        av_measurment_period = all_time / count_of_measurements
        av_sampiling_rate = 1 / av_measurment_period
        quant_step = 3.3 / (2 ** 8)

        # Сохранение данных в файл
        with open('data.txt', 'w') as out_file:
            out_file.write('\n'.join(map(str, data['voltage'])))
        
        # Сохранение конфигурации в файл
        with open('settings.txt', 'w') as settings_file:
            settings_file.write(f'{av_sampiling_rate}\n')
            settings_file.write(f'{quant_step}')

        print(f'Средний период одного измерения составил: {av_measurment_period:.4f} секунд.')
        print(f'Средняя частота дискретизации составила: {av_sampiling_rate:.4f} герц.')
        print(f'Шаг квантования АЦП составляет {quant_step:.4f} вольт.')

        plt.show()

    finally:
        gpio_close(out_pins)