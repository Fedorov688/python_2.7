#!/usr/bin/python
# coding=utf-8
import commands
import time
from datetime import datetime

numbersGPU = 1
name_of_GPU = "1e82"  # or TITAN or 1d81 or 1080 or 1b80 or Tesla or another shit
k = int(commands.getoutput("lspci | grep " + name_of_GPU + " |wc -l"))  # кол - во ГУ для сборки в единый файл
shet_circle = 30000  # кол-во замеров всего
timeout = 3  # пауза между замерами, сек
POWEROFF = False  # Выключить сервер по окончанию? True or False
PEAK_VALUE = [95, 2000, 280, 95]  # [Temperature, Graphics clock, Power Draw, Fan Speed]
CHECK_CPU_T = False


def poweroff():
    if POWEROFF:
        commands.getoutput("poweroff")


def write_error_message(message):
    """Запись сообщения об ошибке с описанием в общую папку"""
    commands.getoutput("mkdir " + str(current_dir[:]) + "/error_message")
    commands.getoutput("mkdir " + str(current_dir[:]) + "/error_message/" + str(name_host[:]))
    commands.getoutput("mkdir " + str(current_dir[:]) + "/error_message/" + str(name_host[:]) + "/" + time_to_start)
    t = open(str(current_dir[:]) + "/error_message/" + str(name_host[:]) + "/" +
             time_to_start + "/" + "/errors.txt", "a")
    t.write(message + '\n')
    t.close()
    c = open(str(current_dir[:]) + "/error_message/" + "common_errors.log", "a")
    c.write("Ошибка на модуле {}. Время старта теста {}. Сообщение: \n{}\n".format(
        str(name_host[:]), time_to_start, message))
    c.close()


def check_gpu(default_numbersgpu, pci_numbersgpu):
    """Проверка Количества GPU"""
    nv_smi_numbersgpu = int(commands.getoutput("nvidia-smi -a | grep 'GPU 0000' | wc -l"))
    if pci_numbersgpu == default_numbersgpu and nv_smi_numbersgpu == default_numbersgpu:
        print('pci_numbersgpu = ' + str(pci_numbersgpu) +
              ' (done!)\nnv_smi_numbersgpu = ' + str(nv_smi_numbersgpu) + ' (done!)\n')
    else:
        print('pci_numbersgpu = ' + str(pci_numbersgpu) +
              ' (error!)\nnv_smi_numbersgpu = ' + str(nv_smi_numbersgpu) + ' (error!)\n')
        messages = 'pci_numbersgpu = ' + str(pci_numbersgpu) + \
                   ' (error!)\nnv_smi_numbersgpu = ' + str(nv_smi_numbersgpu) + ' (error!)\n'
        write_error_message(message=messages)
        poweroff()
        exit(0)


def check_value(value, name_of_value, number_of_value, number_gpu):
    """Проверка данных с GPU на превышение норм
    [Temperature, Graphics clock, Power Draw, Fan Speed]"""
    global PEAK_VALUE
    if float(value) > float(PEAK_VALUE[number_of_value]):
        print("GPU {} is Freak! {} > {}. (Error! Stop it NOW!!!)".format(number_gpu,
                                                                         name_of_value,
                                                                         PEAK_VALUE[number_of_value]))
        messages = "GPU {} is Freak! {} > {}. (Error! Stop it NOW!!!)".format(number_gpu,
                                                                              name_of_value,
                                                                              PEAK_VALUE[number_of_value])
        write_error_message(message=messages)
        poweroff()
        exit(0)


def data(gpu_data, key_gpu):
    """работа с массивом gpu_data(вирт копией среза tmp.txt)"""
    list_name_index = ['GPU Current Temp', 'Graphics', 'Power Draw', 'Fan Speed']
    list_index_value = [4, 2, 3, 3]
    list_name_of_value = ['Temperature GPU', 'Graphics clock', 'Power Draw', 'Fan Speed']
    tmp = ""
    for i in range(len(list_name_index)):
        loc = gpu_data.index(list_name_index[i])
        value = clear_value(gpu_data[loc:loc + 50].split()[list_index_value[i]])
        check_value(value=value, name_of_value=list_name_of_value[i], number_of_value=i, number_gpu=key_gpu)
        tmp += value + ', '
    tmp += '; '
    writers_data(param_name="res", key=key_gpu, value=tmp, wr_mode='a')


def clear_value(value):
    """Избавление от неугодных"""
    useful_char = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ",", ":", ";", " "]
    tmp = ""
    for word in value:
        if word in useful_char:
            tmp += word
    return tmp


def writers_data(param_name, key, value, wr_mode):
    """Запись входных параметров по абсолютному адресу с созданием названия"""
    print(clear_value(value))
    t = open(str(current_dir[:]) + "/" + str(name_host[:]) + "/" +
             time_to_start + "/" + str(param_name) + str(key) + ".txt", wr_mode)
    t.write(clear_value(value) + '\n')
    t.close()


def init_gpu(proc2, key_gpu):
    """Создание файлов для записи логов, обозначение разъема ГУ"""
    writers_data(param_name="tmp", key=key_gpu, value=proc2, wr_mode='w')


def serial_gpu(mas3, key_gpu):
    """Сбор серийников"""
    sn_loc = mas3.index('Serial Number')
    sn_value = mas3[sn_loc + 34:sn_loc + 48]
    print(sn_value)
    writers_data(param_name="serial", key=key_gpu, value=sn_value, wr_mode='a')


def amb_temperature():
    """Входная температура воздуха у сервера"""
    amb_loc = commands.getoutput('ipmitool sdr type temperature | grep Amb')
    amb_value = amb_loc[38:40]
    writers_data(param_name="amb", key=0, value=amb_value, wr_mode='a')


def initial_gpu():
    """Создание временного файла, с содержанием данных о ГУ"""
    commands.getoutput("nvidia-smi -a >" +
                       str(current_dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + "/tmp.txt")

    mas0 = commands.getoutput("cat " + str(current_dir[:]) + "/" + str(name_host[:]) +
                              "/" + time_to_start + "/tmp.txt | grep 'GPU 0000'")
    mas1 = [0, 21, 42, 63, 84, 105, 126, 147]
    mas11 = [20, 41, 62, 83, 104, 125, 146, 167]
    # "инициализация" ГУ
    for key_gpu in range(int(k)):
        print(key_gpu)
        proc2 = mas0[int(mas1[key_gpu]):int(mas11[key_gpu])]
        mas3 = commands.getoutput(
            "cat " + str(current_dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + "/tmp.txt | grep '" + str(
                proc2) + "' --after-context=177")
        init_gpu(proc2, key_gpu)
        serial_gpu(mas3, key_gpu)


def monit():
    global name_of_GPU
    proc1 = commands.getoutput('lspci | grep ' + name_of_GPU + ' |wc -l')
    proc1_1 = commands.getoutput('ipmitool sdr type temperature | grep CPU | wc -l')  # for ipmitools
    mas0 = commands.getoutput("cat " + str(current_dir[:]) + "/" + str(name_host[:]) +
                              "/" + time_to_start + "/tmp.txt | grep 'GPU 0000'")
    mas1 = [0, 21, 42, 63, 84, 105, 126, 147]
    mas11 = [20, 41, 62, 83, 104, 125, 146, 167]
    shet_1 = 0
    while shet_1 < shet_circle:
        commands.getoutput('nvidia-smi -a >' +
                           str(current_dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + "/tmp.txt")
        # Проход по каждой ГУ, создание среза с tmp.txt, обращение к функции data для записи данных
        for key_gpu in range(int(proc1)):
            proc2 = mas0[int(mas1[key_gpu]):int(mas11[key_gpu])]
            mas3 = commands.getoutput("cat " + str(current_dir[:]) + "/" + str(name_host[:]) +
                                      "/" + time_to_start + "/tmp.txt | grep '" + str(proc2) + "' --after-context=170")
            data(gpu_data=mas3, key_gpu=key_gpu)
        if CHECK_CPU_T:
            # mas3_3 = commands.getoutput('sensors | grep Physical') # for sensors
            mas3_3 = commands.getoutput('ipmitool sdr type temperature | grep CPU')  # for ipmitools
            for key_cpu in range(int(proc1_1)):
                mas1_1 = [37, 88]  # [16, 79] # for sensors
                mas11_1 = [40, 91]  # [20, 83] # for sensors
                cpu_value = mas3_3[int(mas1_1[key_cpu]):int(mas11_1[key_cpu])]
                # print(cpu_value)
                writers_data(param_name="cpu", key=key_cpu, value=cpu_value, wr_mode='a')

        print(datetime.now())
        time.sleep(timeout)
        shet_1 += 1


def association_txt():
    """Обработка данных, объединение в единый файл result.txt"""
    common_tmp = []
    schet = 0  # номер строки
    for i in range(k):
        tmp = open(str(current_dir[:]) + "/" + str(name_host[:]) + "/" +
                   time_to_start + '/' + 'res' + str(i) + '.txt', 'r')
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
    result = open(str(current_dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start + '/' + 'result.txt', 'w')
    result.write(common_result)


current_dir = commands.getoutput('pwd')
name_host = commands.getoutput('uname -n')
time_to_start = datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S")
make_host_dir = commands.getoutput('mkdir ' + str(current_dir[:]) + "/" + str(name_host[:]))
make_dir = commands.getoutput('mkdir ' + str(current_dir[:]) + "/" + str(name_host[:]) + "/" + time_to_start)
initial_gpu()
check_gpu(default_numbersgpu=numbersGPU, pci_numbersgpu=k)
print(current_dir[:])
print(name_host[:])
try:
    amb_temperature()
    monit()
except KeyboardInterrupt:
    association_txt()
association_txt()
print('end')
poweroff()
exit(0)
