from model import *
import sys
import os
import subprocess
import fcntl
import termios
import time
from threading import Thread
import multiprocessing
import filecmp
import difflib
from difflib import Differ

def test_instructions():
    run_system([0], "output_system.txt")
    run_model([0], "output_model.txt", [])

    assert(check_output_lines(0,7))

def test_initial_values():
    run_system([], "output_system.txt")
    run_model([], "output_model.txt", "")
    assert(check_number_of_values())


def check_output_lines(startline, endine):
    with open('output_model.txt') as file_1:
        file_1_text = file_1.readlines()
        with open('output_system.txt') as file_2:
            file_2_text = file_2.readlines()
            for x in range(startline,endine):
                print(file_1_text[x])
                print(file_2_text[x])
                if(not(file_1_text[x] == file_2_text[x])):
                    file_1.close()
                    file_2.close()
                    return False
            file_1.close()
            file_2.close()
            return True

def check_number_of_values():
    with open('output_model.txt') as file_1:
        file_1_text = file_1.readlines()
        with open('output_system.txt') as file_2:
            file_2_text = file_2.readlines()
            line1 = file_1_text[10]
            line2 = file_2_text[10]

            values_model = get_values(line1)
            values_system = get_values(line2)
            if(not len(values_model) == len(values_system)):
                file_1.close()
                file_2.close()
                return False
            file_1.close()
            file_2.close()
            return True

def check_values():
    with open('output_model.txt') as file_1:
        file_1_text = file_1.readlines()
        with open('output_system.txt') as file_2:
            file_2_text = file_2.readlines()
            line1 = file_1_text[10]
            line2 = file_2_text[10]

            values_model = get_values(line1)
            values_system = get_values(line2)

            for x in range(len(values_model)):
                if(not(values_model[x] == values_system[x])):
                    file_1.close()
                    file_2.close()
                    return False
            file_1.close()
            file_2.close()
            return True

def get_values(line):
    all_values = []
    value = ""
    at_value = False
    for x in range(len(line)):
        if((not at_value) and not(line[x] == " ")):
            value = line[x]
            at_value = True
        elif(at_value and not(line[x] == " ")):
            value = value + line[x]
        elif(at_value and (line[x] == " ")):
            all_values.append( value)
            at_value = False
    all_values.append( value)
    return all_values

def check_output(file1, file2):
    with open(file1) as file_1:
        file_1_text = file_1.readlines()

    with open(file2) as file_2:
        file_2_text = file_2.readlines()
    result = True
    # Find and print the diff:
    for line in difflib.unified_diff(
            file_1_text, file_2_text, fromfile='file1.txt',
            tofile='file2.txt', lineterm=''):
        result = False
    file_1.close()
    file_2.close()
    return result

#Function to run on thread, will run the js file
def run_thread(file):
    string = 'node ../legacy_system/node/ll.js > ' + file
    os.system(string)

#Takes a list with fuel as input and will run the system with this input
#Places all output from the system in the specified file
def run_system(list, file):
    proc = multiprocessing.Process(target=run_thread, args=(file, ))
    proc.start()
    if(list == []):
        time.sleep(1)
        proc.join()
        proc.terminate()
    with open('/dev/ttys002', 'w') as fd:
        for fuel in list:
            time.sleep(1)
            string = str(fuel) + "\n"
            for c in string:
                fcntl.ioctl(fd, termios.TIOCSTI, c)
    fd.close()
    time.sleep(1)
    proc.join()
    ss
    proc.terminate()

def run_thread_model(file, args):
    string = 'python3 model.py ' + str(args) + ' > ' + file
    os.system(string)

def run_model(list, file, args):
    proc = multiprocessing.Process(target=run_thread_model, args=(file, args, ))
    proc.start()
    time.sleep(1)
    proc.join()
    proc.terminate()

def test_suit():
    #test_instructions()
    test_initial_values()

if __name__ == "__main__":
    test_suit()
