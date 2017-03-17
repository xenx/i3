#!/usr/bin/env python
# -*- coding: utf-8 -*-

METADATA_FILE = '/tmp/mplayer.data'
SONG_COLOR = '#6780fb'
NOSONG_COLOR = '#ffffff'
NOSONG_MSG = 'No Song Played'

from time import sleep
import sys
from subprocess import Popen, PIPE

def run_command(command):
    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    return str(output.decode())

def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + '\n')
    sys.stdout.flush()

def get_volume():
    now_volume = run_command(['amixer'])
    now_volume = now_volume.split('\n')[5][-10:].split('[')[1].replace('] ', '').replace('%', '')
    try:    
        now_volume = int(now_volume)
    except ValueError:
        return ' '

    if now_volume in range(0, 20): now_volume = ' '
    if now_volume in range(20, 60): now_volume = ' '
    if now_volume in range(60, 101): now_volume = ' '

    return now_volume

def get_battery():
    battery = run_command(['acpi'])
    charging = bool("Charging," in battery)
    battery = battery.split(':')[1].split(',')[1].replace(' ', '').replace('%', '')
    battery = int(battery)

    if battery in range(0, 20): battery = ' '
    if battery in range(20, 60): battery = ' '
    if battery in range(60, 80): battery = ' '
    if battery in range(80, 101): battery = ' '
    if charging:
        battery = battery + " "

    return battery

def get_time():
    time = run_command(['date', '+%H:%M'])
    return time.replace('\n', '') + "  "

def get_day():
    day = run_command(['date', '+%m-%d'])
    return day.replace('\n', '') + "  "

if __name__ == '__main__':
    while True:
        print_line(get_day() + ' | ' + get_time() + ' | ' + get_volume() + ' | ' + get_battery())
        sleep(1)
