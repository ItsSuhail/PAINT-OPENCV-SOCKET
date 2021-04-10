"""
Start- 9th April 2021: 6:50 PM
--Made by Suhail Hasan--
"""
#
"""
IMPORTING MODULES:
"""
import socket
import cv2
import pickle
import struct
import time
import sys
"""
CLIENT WORK
"""
CLIENT_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOSTNAME = str(input("ENTER YOUR IP: "))
if not HOSTNAME:
    HOSTNAME = socket.gethostbyname(socket.gethostname())
PORT = int(input("ENTER YOUR PORT: "))
if not PORT:
    PORT = 5555
CLIENT_SOCKET.connect((HOSTNAME,PORT))
"""
GETTING DATA FROM SERVER
"""
data = b""
payload_size = struct.calcsize("Q")
try:
    while True:
        while len(data) < payload_size:
            packet = CLIENT_SOCKET.recv(4*1024) # 4K
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += CLIENT_SOCKET.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("PAINT--RECEIVING",frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            break
except socket.error as exc:
    print("SOCKET ERROR: ",exc)
    CLIENT_SOCKET.close()
    time.sleep(10)
    sys.exit()
CLIENT_SOCKET.close()
time.sleep(10)
sys.exit()
