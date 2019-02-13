#! usr/bin/env python3


import socket
import subprocess
import time
import os




def OrderTaker():
    s = socket.socket()
    host = '192.168.43.208'
    port = 5000

    while True:
        try:
            s.connect((host,port))
            print("Connected")
        except:
            pass

        try:
            data = s.recv(1024).decode()
            if (data == "Sending"):
                with open('Order_file.txt', 'wb') as f:
                    print("File opened")
                    while True:
                        print("Receiving Data....")
                        data = s.recv(1024)

                        print("Successfully get the file")
                        f.write(data)
                        f.close()

                        os.system('python printing.py')
                        print("Printing Complete")
                        break


        except:
            pass



OrderTaker()
