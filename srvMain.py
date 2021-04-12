"""
Start- 9th April 2021: 6:50 PM
--Made by Suhail Hasan--

https://github.com/ItsSuhail/PAINT-OPENCV-SOCKET
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
import sys
import time
"""
SERVER WORK:
"""
SERVER_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOSTNAME = socket.gethostbyname(socket.gethostname())
PORT = int(input("ENTER YOUR PORT: "))
if not PORT:
    PORT = 5555
PORT = int(PORT)
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
DEFINING IMAGE FOR TRACKBAR
"""
#
IMAGE_TB = numpy.zeros((150,410,3),numpy.uint8)
cv2.namedWindow('PAINT-COLOR')
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
SHOW = False
"""
DEFINING ONCALLBACK
"""
#
def onCallBack(event,x,y,flags,params):
    global current_former_x,current_former_y,DRAW, MODE, IMAGE, SHOW
    if event == cv2.EVENT_RBUTTONDBLCLK:
        imageColor(IMAGE,255,255,255)
    if event == cv2.EVENT_RBUTTONDOWN:
        imageColor(IMAGE,B,G,R)
    if event == cv2.EVENT_RBUTTONUP or event == cv2.EVENT_LBUTTONUP:
        SHOW = True
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
    global SHOW
    PickleIMG = pickle.dumps(IMAGE)
    Struct_Img = struct.pack("Q",len(PickleIMG))+PickleIMG
    try:
        CLIENT.sendall(Struct_Img)
        SHOW = False
    except socket.error as exc:
        print("I think that socket is closed! Error: ",exc)
        sys.exit()
        
"""
DECLARING FUNCTION TO START THREADING
"""
#
def startThreadSI(IMG,CLNT):
    thread = threading.Thread(target=sendImg,args=[IMG,CLNT])
    thread.start()
"""
DEFINING NOTHING FUNCTION FOR WORKING OF TRACKBAR
"""
#
def nothing(x):
    pass
"""
ALL DONE, CREATING WHILE LOOP
"""
try:
    start_srv()
    client_socket,addr = SERVER_SOCKET.accept()
    print('GOT CONNECTION FROM:',addr)
except socket.error as exc:
    print("SOCKET ERROR: ",exc)
cv2.setMouseCallback("PAINT",onCallBack)
"""
DEFINING TRACKBAR
"""
cv2.createTrackbar('B','PAINT-COLOR',0,255,nothing)
cv2.createTrackbar('G','PAINT-COLOR',0,255,nothing)
cv2.createTrackbar('R','PAINT-COLOR',0,255,nothing)
"""
SHOWING THE IMAGES
"""
cv2.imshow("PAINT",IMAGE)
cv2.imshow("PAINT-COLOR",IMAGE_TB)
try:
    while True:
        B = cv2.getTrackbarPos('B','PAINT-COLOR')
        G = cv2.getTrackbarPos('G','PAINT-COLOR')
        R = cv2.getTrackbarPos('R','PAINT-COLOR')
        IMAGE_TB[:] = [B,G,R]
        cv2.imshow("PAINT-COLOR",IMAGE_TB)
        if client_socket and SHOW:
            sendImg(IMAGE, client_socket)
        k = cv2.waitKey(1)
        if k & 0xff == ord('q'):
            break
except socket.error as exc:
    print("SOCKET ERROR: ",exc)

cv2.destroyAllWindows()
time.sleep(10)
sys.exit()
