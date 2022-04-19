import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt


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
    current_voltage = round((int(b, 2)) * 3.3 / 256, 3)

    print(f"Current voltage -> {current_voltage}")

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
    dac = [10, 9, 11, 5, 6, 13, 19, 26][::-1]
    leds = [21, 20, 16, 12, 7, 8, 25, 24][::-1]
    comp = 4
    troyka = 17

    inp_pins = [comp]
    out_pins = dac + leds + [troyka]

    gpio_init(inp_pins, out_pins)

    try:
        data = {
            'voltage': [],
            'time': []
        }
        start_time = time.time()

        troyka_reg('on')

        capacitor_charge = analog_to_digital_conventer() / 3.3

        while capacitor_charge < 0.94:
            cur_voltage = analog_to_digital_conventer()
            cur_time = time.time() - start_time
            data['voltage'].append(cur_voltage)
            data['time'].append(cur_time)

            capacitor_charge = cur_voltage / 3.3
            led_indicator(capacitor_charge * 100)
            time.sleep(0.1)
        
        troyka_reg('off')

        while capacitor_charge > 0.02:
            cur_voltage = analog_to_digital_conventer()
            cur_time = time.time() - start_time
            data['voltage'].append(cur_voltage)
            data['time'].append(cur_time)

            capacitor_charge = cur_voltage / 3.3
            led_indicator(capacitor_charge * 100)
            time.sleep(0.1)
        
        all_time = cur_time

        print(f'Эксперимент завершён!\nОбщая продолжительность эксперимента составила: {all_time} секунд.')
        
        # Построения графика зависимости напряжения на обкладках конденсатора от времени
        plt.plot(data['time'], data['voltage'])
        plt.xlabel('t, с')
        plt.ylabel('U, В')
        plt.title('Зависимость напряжения на обкладках конденсатора U от времени t')
        plt.show()

        # Вычисление некоторых параметров эксперимента
        count_of_measurements = len(data['time'])
        av_measurment_period = all_time / count_of_measurements
        av_sampiling_rate = 1 / av_measurment_period
        quant_step = 3.3 / (2 ** 8)

        # Сохранение данных в файл
        with open('data.txt', 'w') as out_file:
            out_file.write('voltage,time\n')

            for i in range(count_of_measurements):
                voltage = data['voltage'][i]
                time = data['time'][i]
                out_file.write(f'{voltage},{time}\n')
        
        # Сохранение конфигурации в файл
        with open('settings.txt', 'w') as settings_file:
            settings_file.write(f'Average sampiling rate: {av_sampiling_rate}\n')
            settings_file.write(f'Quantization step: {quant_step}\n')

        # Вывод технической информации в терминал
        print(f'Средний период одного измерения составил: {av_measurment_period} секунд.')
        print(f'Средняя частота дискретизации составила: {av_sampiling_rate} герц.')
        print(f'Шаг квантования АЦП составляет {quant_step}')

    finally:
        gpio_close(out_pins)