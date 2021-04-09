"""
Start- 9th April 2021: 6:50 PM
--Made by Suhail Hasan--
"""
#
"""
IMPORTING MODULES:
"""
import cv2
import socket
import pickle
import struct
import numpy
import threading
"""
SERVER WORK:
"""
SERVER_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOSTNAME = socket.gethostbyname(socket.gethostname())
PORT = 5555
print("HOST IP: ",HOSTNAME, " HOST PORT: ", PORT)
SOCKET_ADDRESS = (HOSTNAME,PORT)
def start_srv():
    SERVER_SOCKET.bind(SOCKET_ADDRESS)
    SERVER_SOCKET.listen(1)
    print("[SERVER] is now listening")

"""
DEFINING IMAGE
"""
#
IMAGE = numpy.zeros((512,512,3),numpy.uint8)
IMAGE[:] = [255,255,255]
cv2.namedWindow('PAINT')
"""
DEFINING COLORS
"""
#
B = 0
G = 0
R = 0
"""
DEFINING FUNCTIONS FOR SETTING COLORS
"""
#
def imageColor(img,B,G,R):
    img[:] = [B,G,R]
"""
DEFINING VARIABLES FOR DRAWING
"""
#
DRAW = False
MODE = True
"""
DEFINING ONCALLBACK
"""
#
def onCallBack(event,x,y,flags,params):
    global current_former_x,current_former_y,DRAW, MODE, IMAGE
    if event == cv2.EVENT_RBUTTONDBLCLK:
        imageColor(IMAGE,255,255,255)
    if event == cv2.EVENT_RBUTTONDOWN:
        imageColor(IMAGE,B,G,R)
    if event == cv2.EVENT_LBUTTONDOWN:
        DRAW = True
        current_former_x,current_former_y=x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if DRAW == True:
            if MODE == True:
                cv2.line(IMAGE,(current_former_x,current_former_y),(x,y),(B,G,R),5)
                current_former_x = x
                current_former_y = y
    elif event==cv2.EVENT_LBUTTONUP:
        DRAW=False
        if MODE==True:
            cv2.line(IMAGE,(current_former_x,current_former_y),(x,y),(B,G,R),5)
            current_former_x = x
            current_former_y = y
    
    cv2.imshow("PAINT",IMAGE)
"""
DEFINING FUNCTION FOR SENDING IMAGE CONTINOUSLY
"""
#
def sendImg(IMAGE,CLIENT):
    PickleIMG = pickle.dumps(IMAGE)
    Struct_Img = struct.pack("Q",len(PickleIMG))+PickleIMG
    CLIENT.sendall(Struct_Img)
"""
DECLARING FUNCTION TO START THREADING
"""
#
def startThreadSI(IMG,CLNT):
    thread = threading.Thread(target=sendImg,args=[IMG,CLNT])
    thread.start()

"""
ALL DONE, CREATING WHILE LOOP
"""
start_srv()
client_socket,addr = SERVER_SOCKET.accept()
print('GOT CONNECTION FROM:',addr)
cv2.setMouseCallback("PAINT",onCallBack)
cv2.imshow("PAINT",IMAGE)
while True:
    if client_socket:
        startThreadSI(IMAGE, client_socket)
        cv2.waitKey(1)


cv2.destroyAllWindows()
