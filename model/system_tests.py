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
    run_model([], "output_model.txt", "")

    assert(check_output_lines(0,7))

def test_initial_values():
    run_system([], "output_system.txt")
    run_model([], "output_model.txt", "")
    assert(check_number_of_values())
    assert(check_values())

def test_wrong_input_format():
    run_system(["x"], "output_system.txt")
    run_model([], "output_model.txt", "x")
    assert(check_number_of_values())
    assert(check_values())

    time.sleep(1)

    run_system(["x*"], "output_system.txt")
    run_model([], "output_model.txt", "x*")
    assert(check_number_of_values())
    assert(check_values())

    time.sleep(1)

    run_system([","], "output_system.txt")
    run_model([], "output_model.txt", ",")
    assert(check_number_of_values())
    assert(check_values())

def test_invalid_input():
    run_system([1], "output_system.txt")
    run_model([], "output_model.txt", "1")
    assert(check_number_of_values())
    assert(check_values())

    time.sleep(1)

    run_system([7], "output_system.txt")
    run_model([], "output_model.txt", "7")
    assert(check_number_of_values())
    assert(check_values())

    time.sleep(1)

    run_system([-1], "output_system.txt")
    run_model([], "output_model.txt", "-1")
    assert(check_number_of_values())
    assert(check_values())

    time.sleep(1)

    run_system([201], "output_system.txt")
    run_model([], "output_model.txt", "201")
    assert(check_number_of_values())
    assert(check_values())


def test_number_of_outputs():
    run_system([10], "output_system.txt")
    run_model([], "output_model.txt", "10")
    assert(check_number_of_values())

    run_system([10,10], "output_system.txt")
    run_model([], "output_model.txt", "10 10")
    assert(check_number_of_values())

    run_model([], "output_model.txt", "10 10 10 10 10 10")
    run_system([10,10,10,10,10,10], "output_system.txt")
    assert(check_number_of_values())

def test_game_ending():
    run_system([200, 200, 200, 200, 200, 200, 200, 200], "output_system.txt")
    run_model([], "output_model.txt", "200 200 200 200 200 200 200 200")
    assert(check_output_lines(12,13))

def check_output_lines(startline, endine):
    with open('output_model.txt') as file_1:
        file_1_text = file_1.readlines()
        with open('output_system.txt') as file_2:
            file_2_text = file_2.readlines()
            for x in range(startline,endine):
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
                print( len(values_model))
                print(len(values_system))
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
                    #for y in range(len(values_model[x])):
                    #    if(not(values_model[x][y] == values_system[x][y])):
                    #        print("-")
                    print(values_model[x])
                    print(values_system[x])
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
    #global pid
    #pid = os.getpid()
    string = 'node ../legacy_system/node/ll.js > ' + file
    os.system(string)

#Takes a list with fuel as input and will run the system with this input
#Places all output from the system in the specified file
def run_system(list, file):
    proc = multiprocessing.Process(target=run_thread, args=(file, ))
    proc.start()
    if(list == []):
        time.sleep(1)
        proc.terminate()
        proc.join()

    count = 0
    with open('/dev/ttys002', 'w') as fd:
        for fuel in list:
            count = count + 1
            print("---")
            time.sleep(3)
            string = str(fuel) + "\n"
            for c in string:
                fcntl.ioctl(fd, termios.TIOCSTI, c)
    print(count)
    #global pid
    #string = 'kill -INT ' + pid
    #os.system(string)
    fd.close()
    time.sleep(1)
    proc.terminate()
    proc.join()

def run_thread_model(file, args):
    string = 'python3 model.py ' + str(args) + ' > ' + file
    os.system(string)

def run_model(list, file, args):
    proc = multiprocessing.Process(target=run_thread_model, args=(file, args, ))
    proc.start()
    time.sleep(1)
    proc.terminate()
    proc.join()

def test_suit():
    #test_instructions()
    #test_initial_values()
    #test_wrong_input_format()
    #test_invalid_input()
    #test_number_of_outputs()
    test_game_ending()

if __name__ == "__main__":
    test_suit()
