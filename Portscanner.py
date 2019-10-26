#!/bin/python3

import sys 
import socket
import threading
from queue import Queue
from datetime import datetime

print_lock = threading.Lock()
t1 = datetime.now()

#Define our target 
if len(sys.argv) == 2:
	target = socket.gethostbyname(sys.argv[1]) #Translate a host name to IPV4
else:
	print("Invalid amount of arguments.")
	print("Syntax: python3 Portscanner.py <ip>")
	sys.exit()

#Add banner
print("-" *50)
print("Scanning target "+target)
print("Time started: "+str(datetime.now()))
print("-" *50)

start = int (input("Enter The Port From Where You Want to start: "))
stop = int (input("Enter End Port: "))
speed = int ((stop - start) + 1)

def scan(port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1) #is a float
		result=s.connect_ex((target,port)) #return error indicator
		#print("Checking port {}".format(port))
		if result == 0:
			with print_lock:
				print("Port {} is open".format(port))
		s.close()

	except KeyboardInterrupt:
		print("\nExiting Program.")
		sys.exit()

	except socket.gaierror:
		print("Hostname could not be resolved.")
		sys.exit()

	except socket.error:
		print("Couldn't connect to server.")
		sys.exit()

def Threader():
	while True:
		worker = q.get()
		scan(worker)
		q.task_done()
q = Queue()

for i in range(speed):
	t = threading.Thread(target=Threader)
	t.daemon = True
	t.start()
	
for x in range (start,stop+1):
	q.put(x)

q.join()

t2 = datetime.now()
total =  t2 - t1
print ("Scanning Completed in: "+str(total))