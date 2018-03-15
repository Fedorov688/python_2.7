# -*- coding: utf-8 -*-
import os
import time
import threading

start_time = time.time()
# "icc --version",
# "icc",
COMMANDs = ["dmidecode --type 4", "uname -a", "cat /etc/*rele*", "gcc --version", "mpirun -V", "nvidia-smi",
            "nvcc -V", 'dmidecode --type 17 | grep "Size"', "fdisk -l"]
KEYWORDs = ["Version:", " ", "PRETTY_NAME", "gcc", "MPI", "Driver Version", "release", "B", "Disk /dev/"]


def command_pars(command, file_out):
    command += " > {}"
    os.system(command.format(file_out))


def read_file(name_of_file, keyword):
    file = open(name_of_file)
    for line in file:
        if keyword in line:
            print(line)


i = 0
for COMMAND in COMMANDs:
    a_0 = threading.Thread(target=command_pars, args=(COMMAND, str(i)))
    i += 1
    a_0.start()
while threading.active_count() > 1:
    time.sleep(0.000001)
print("Finished")

for i in range(len(COMMANDs)):
    read_file(str(i), KEYWORDs[i])
    os.remove(str(i))

res_time = time.time() - start_time
print("отработало за {} секунд!".format(res_time))
