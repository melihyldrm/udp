from raspicontrol import BluetoothDevice
#from mindwavecalisan import MindWaveMobileThread
from typing import Union
from fastapi import FastAPI, BackgroundTasks
import uvicorn
from fastapi.responses import JSONResponse
import random
import socket
from fastapi.middleware.cors import CORSMiddleware
import threading, time
from itertools import cycle


app = FastAPI()

origins = [
    "*"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

UDP_IP = "192.168.0.193"
UDP_PORT = 8000

@app.get("/stream")
def udp_server_task():
    server_thread = threading.Thread(target=thread_stream)
    server_thread.start()
    return "OK"

def thread_stream():
    address = (UDP_IP, UDP_PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # server_socket.bind((UDP_IP, UDP_PORT))
    rand1_values = cycle([1, 2])
    while True:
        rand1 = next(rand1_values)
        rand2 = random.randint(0, 15)
        rand3 = random.randint(0, 15)
        rand4 = random.randint(0, 15)
        # Convert the 4-bit number to a byte (8-bit) representation
        rand_byte1 = rand1.to_bytes(1, "big")
        rand_byte2 = rand2.to_bytes(1, "big")
        rand_byte3 = rand3.to_bytes(1, "big")
        rand_byte4 = rand4.to_bytes(1, "big")
        # Create a new byte with the same value but repeating 4 times
        combined_byte = rand_byte1+rand_byte2+rand_byte3+rand_byte4
        print(combined_byte)
        # Send the combined byte to the server
        server_socket.sendto(combined_byte, address)
        time.sleep(1)

                
if __name__ == '__main__':
    uvicorn.run(app, host='192.168.0.193', port=8000)