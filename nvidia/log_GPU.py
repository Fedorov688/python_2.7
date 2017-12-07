#!/usr/bin/python
# coding=utf-8
import commands
import time
from datetime import datetime
from string import maketrans


name_of_GPU = "TITAN"  # or TITAN or 1080 or Tesla or another shit
k = int(commands.getoutput('lspci | grep ' + name_of_GPU + ' |wc -l'))  # кол - во ГУ для сборки в единый файл
shet_circle = 3  # кол-во замеров всего
timeout = 1  # пауза между замерами, сек


def data(mas3, key_gpu):
    """работа с массивом mas3(вирт копией среза tmp.txt)"""
    # значение температуры Ядра ГУ
    tm_loc = mas3.index('GPU Current Temp')
    tm_value = mas3[tm_loc + 30:tm_loc + 33]
    print(tm_value)
    # записываем в log значение температуры Ядра ГУ
    # writers_data(tm, key_gpu, tm_value, wr_mode='a')

    # значение частоты Ядра ГУ
    cl_loc = mas3.index('Graphics')
    cl_value = mas3[cl_loc + 29:cl_loc + 35]
    # print(cl_value)
    # записываем в log значение частоты Ядра ГУ
    # writers_data(cl, key_gpu, cl_value, wr_mode='a')

    # значение энергопотребления ГУ
    wt_loc = mas3.index('Power Draw')
    wt_value = mas3[wt_loc + 29:wt_loc + 36]
    # print(wt_value)

    # значение Fan Speed ГУ
    fn_loc = mas3.index('Fan Speed')
    fn_value = mas3[fn_loc + 34:fn_loc + 37]
    print(fn_value)


    # записываем в log значение энергопотребления ГУ
    # writers_data(wt, key_gpu, wt_value, wr_mode='a')
    result1 = tm_value + ', ' + cl_value + ', ' + wt_value + ', ' + fn_value + '; '
    writers_data(res, key_gpu, result1, wr_mode='a')
    # print(result1)


def clear_value(value):
    """Избавление от неугодных"""
    result1 = value.replace("M", "")
    result2 = result1.replace("W", "")
    result3 = result2.replace("+", "")

    return result3


def writers_data(param_name, key_gpu, value, wr_mode):
    """Запись входных параметров по абсолютному адресу с созданием названия"""
    print(clear_value(value))
    t = open(str(dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + "/" + param_name(key_gpu), wr_mode)
    t.write(clear_value(value) + '\n')
    t.close()


def init_gpu(proc2, key_gpu):
    """Создание файлов для записи логов, обозначение разъема ГУ"""
    mas4 = [res, tm, cl, wt]
    for i in range(1):
        writers_data(mas4[i], key_gpu, proc2, wr_mode='w')


def serial_gpu(mas3, key_gpu):
    """Сбор серийников"""
    sn_loc = mas3.index('Serial Number')
    sn_value = mas3[sn_loc + 34:sn_loc + 48]
    print(sn_value)
    writers_data(param_name=res, key_gpu=key_gpu, value=sn_value, wr_mode='a')


def amb_temperature():
    """Входная температура воздуха у сервера"""
    amb_loc = commands.getoutput('ipmitool sdr type temperature | grep Amb')
    amb_value = amb_loc[38:40]
    writers_data(param_name=amb, key_gpu=0, value=amb_value, wr_mode='a')


# Генерция названия файлов для log'ов
def tm(key_gpu):
    return "temp" + str(key_gpu) + ".txt"
def cl(key_gpu):
    return "cloc" + str(key_gpu) + ".txt"
def wt(key_gpu):
    return "watt" + str(key_gpu) + ".txt"
def res(key_gpu):
    return "res" + str(key_gpu) + ".txt"
def cpu(key_cpu):
    return "cpu" + str(key_cpu) + ".txt"
def amb(key_cpu):
    return "cpu" + str(key_cpu) + ".txt"

def monit():
    # Создание временного файла, с содержанием данных о ГУ
    commands.getoutput('nvidia-smi -a >' + str(dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + "/tmp.txt")
    global name_of_GPU
    proc1 = commands.getoutput('lspci | grep ' + name_of_GPU + ' |wc -l')
    # proc1_1 = commands.getoutput('sensors | grep Physical | wc -l') # for sensors
    proc1_1 = commands.getoutput('ipmitool sdr type temperature | grep CPU | wc -l')  # for ipmitools
    mas0 = commands.getoutput("cat " + str(dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + "/tmp.txt | grep 'GPU 0000'")
    mas1 = [0, 21, 42, 63, 84, 105, 126, 147]
    mas11 = [20, 41, 62, 83, 104, 125, 146, 167]
    # "инициализация" ГУ
    for key_gpu in range(int(k)):
        print(key_gpu)
        proc2 = mas0[int(mas1[key_gpu]):int(mas11[key_gpu])]
        mas3 = commands.getoutput(
            "cat " + str(dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + "/tmp.txt | grep '" + str(
                proc2) + "' --after-context=144")
        init_gpu(proc2, key_gpu)
        serial_gpu(mas3, key_gpu)
    shet_1 = 0
    while shet_1 < shet_circle:
        commands.getoutput('nvidia-smi -a >' + str(dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + "/tmp.txt")
        # Проход по каждой ГУ, создание среза с tmp.txt, обращение к функции data для записи данных
        for key_gpu in range(int(proc1)):
            proc2 = mas0[int(mas1[key_gpu]):int(mas11[key_gpu])]
            mas3 = commands.getoutput("cat " + str(dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + "/tmp.txt | grep '" + str(proc2) + "' --after-context=144")
            data(mas3, key_gpu)
        # mas3_3 = commands.getoutput('sensors | grep Physical') # for sensors
        mas3_3 = commands.getoutput('ipmitool sdr type temperature | grep CPU')  # for ipmitools
        for key_cpu in range(int(proc1_1)):
            mas1_1 = [37, 88]  # [16, 79] # for sensors
            mas11_1 = [40, 91]  # [20, 83] # for sensors
            cpu_value = mas3_3[int(mas1_1[key_cpu]):int(mas11_1[key_cpu])]
            # print(cpu_value)
            writers_data(cpu, key_cpu, cpu_value, wr_mode='a')
        print(datetime.now())
        time.sleep(timeout)
        shet_1 += 1


def association_txt():
    """Обработка данных, объединение в единый файл result.txt"""
    common_tmp = []
    schet = 0  # номер строки
    for i in range(k):
        tmp = open(str(dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + '/' + 'res' + str(i) + '.txt', 'r')
        common_tmp.append(tmp.readlines())
        tmp.close()
    print(common_tmp)

    common_result = ''
    while schet < shet_circle:
        try:
            for i in range(k):
                print(common_tmp[i][schet])
                if i != k-1:
                    common_result += common_tmp[i][schet][:-2] + ' ,'
                else:
                    common_result += common_tmp[i][schet]
                    common_result += '\n'
        except IndexError:
            print('finish')
            schet = shet_circle + 1
        schet += 1
    print(common_result)
    result = open(str(dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + '/' + 'result.txt', 'w')
    result.write(common_result)


dir = commands.getoutput('pwd')
name_host = commands.getoutput('uname -n')
time_to_start = datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S")
make_host_dir = commands.getoutput('mkdir ' + str(dir[:]) + "/" + str(name_host[:]))
make_dir = commands.getoutput('mkdir ' + str(dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start)
print(dir[:])
print(name_host[:])
try:
    amb_temperature()
    monit()
except KeyboardInterrupt:
    association_txt()
association_txt()
print('end')
