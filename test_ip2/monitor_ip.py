# /usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import subprocess
# модуль захвата нажатий
from pynput import keyboard
import time


timeout = 1  # Задержка между итерациями(вызовами команд) в секундах
iters = 5  # Количество итераций
i = 0  # счетчик


def on_release(key):
    """остановка с помощью определенной клавиши"""
    print('{0} released'.format(key))
    if key == keyboard.Key.enter:
        # Stop listener
        print ('stop')
        global i
        i = iters + 1
        return False


def key_pars():
    print('shit')
    lis = keyboard.Listener(on_release=on_release)
    lis.start()
    lis.isDaemon()


def command():
    """выполнение команд"""
    try:
        subprocess.call(['clear'], shell=True)
        subprocess.call(["ls", "-l"], shell=True)
        subprocess.call(["timedatectl"], shell=True)
    finally:
        print('hm1')


def main():
    key_pars()
    global i
    while i < iters:
        try:
            print(i)
            command()
            time.sleep(timeout)
            i += 1
        finally:
            print "Waiting"


main()
print('next step')
