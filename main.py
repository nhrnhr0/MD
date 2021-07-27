

import sys
import os
import signal
import time
import subprocess

import time
from typing import Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import threading



class MyEventHandler():
    observer = None
    my_event_handler = None
    exit_queue_windows = list()
    showing_products = set()
    def __init__(self):
        super(MyEventHandler,self).__init__()
        patterns = ["*.barcodes"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        self.my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        self.my_event_handler.on_created = self.on_created
        self.my_event_handler.on_deleted = self.on_deleted
        self.my_event_handler.on_modified = self.on_modified
        self.my_event_handler.on_moved = self.on_moved
        
        path = "."
        go_recursively = False
        self.my_observer = Observer()
        self.my_observer.schedule(self.my_event_handler, path, recursive=go_recursively)
        self.my_observer.start()
        
        pass
    def on_created(self,event):
        pass
    def on_deleted(self,event):
        pass
    def on_modified(self,event):
        print(f'on_modified: {event.src_path}')
        if event.src_path == '.\\barcode.barcodes':
            self.showing_products.add(self.get_barcode_from_file(event.src_path))
        
        pass
    def on_moved(self,event):
        pass
    
    
    def terminate_process(self, pro):
        print('terminate_process: ', pro.pid)
        pro.terminate()
        
    def exit_all_chromium_product_windows(self):
        for pro in self.exit_queue_windows:
            self.terminate_process(pro)
    
    def exit_chromium_window(self, pro):
        if pro in self.exit_queue_windows:
            self.exit_queue_windows.remove(pro)
            
            self.terminate_process(pro)
        
    def start_chromium_window(self, barcode):
        
        self.exit_all_chromium_product_windows()
        
        cmd =  f'chromium http://127.0.0.1:8010/product/{barcode}/'
        pro = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)#, preexec_fn=os.setsid)
        print('start chromium window', cmd,' pid: ', pro.pid)
        
        self.exit_queue_windows.append(pro)
        t = threading.Timer(5, self.exit_chromium_window, [pro])
        t.start()
        return pro.pid
    
    
    def update(self):
        #print('update - insert: ', self.showing_products,' exit: ', self.exit_queue_windows )
        lbarcodes = list(self.showing_products)
        if len(lbarcodes) > 0:
            barcode = lbarcodes[0]
            pid = self.start_chromium_window(barcode)
            lbarcodes.remove(barcode)
            self.showing_products = set(lbarcodes)
        
        
    

    def get_barcode_from_file(self, path):
        barcode_file = open(path, "r")
        lines = barcode_file.readlines()
        last_line = lines[-1:]
        return last_line[0]

def main():
    handler = MyEventHandler()
    print('listen to files chnage...')
    try:
        while True:
            time.sleep(1)
            handler.update()
    except KeyboardInterrupt:
        handler.my_observer.stop()
        handler.my_observer.join()


if __name__ == '__main__':
        main()