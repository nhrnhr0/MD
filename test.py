import sys
import os
import signal
import time
import subprocess

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler



	
	
def on_created(event):
    print(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")


last_showed_barcode = '123'
def on_modified(event):
    print(f"============================== {event.src_path} has been modified")
    if event.src_path == './barcode.barcodes':
        barcode_file = open(event.src_path, "r")
        lines = barcode_file.readlines()
        last_line = lines[-1:]
        print('last line barcode: ', last_line)
        handle_barcode(last_line[0])
    elif event.src_path == './exit.barcodes':
        exit_file = open(event.src_path, "r")
        lines = exit_file.readlines()
        last_line = lines[-1:]
        print('last line exit: ', last_line[0])
        
        
        barcode_file = open('./barcode.barcodes', "r")
        lines = barcode_file.readlines()
        llbarcode = lines[-1:][0]
        print('llbarcode: ', llbarcode)
        if llbarcode == last_line[0]:
            print('============================== exit chromium')
            exit_chromium()

    ############################
    #
    # your code go here
    #
    ############################


def exit_chromium():
    os.system('pkill -o chromium')
    os.system(f'chromium-browser http://127.0.0.1:8010/ & ')

def handle_barcode(barcode):
    print('open barcode:', barcode)
    last_showed_barcode = barcode
    print(last_showed_barcode)
    #cmd =  f'chromium-browser http://127.0.0.1:8010/product/{barcode}/'
    cmd =  f'chromium http://127.0.0.1:8010/product/{barcode}/'
    pro = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True, preexec_fn=os.setsid)


def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

patterns = ["*.barcodes"]
ignore_patterns = None
ignore_directories = False
case_sensitive = True
my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved


path = "."
go_recursively = False
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)
my_observer.start()


def main():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


if __name__ == '__main__':
        main()
