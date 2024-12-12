import subprocess
import os
import time

msgssh = open("local\logs\msg.out", 'a+')
errssh = open("local\logs\err.err", 'a+')

process = subprocess.Popen(['python'], stdin=subprocess.PIPE,
                           stdout=msgssh, stderr=errssh, shell=True)

while True:
    process.stdin.write(b"print('hello')\r\n")
    # process.stdin.flush()
    msgssh.flush()
    # msg = open("local\logs\msg.out", 'r')
    print("output:", msgssh.read()) 
    time.sleep(1)