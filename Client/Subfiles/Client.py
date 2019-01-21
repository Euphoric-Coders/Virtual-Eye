import socket, pickle, cv2, zlib, struct, select
import numpy as np


def send_txt(txt = ""):
    client = socket.socket()
    host = cur_server
    port = 60000
    client.connect((host,port))
    print("Connected to {0} at port: {1}".format(host,port))
    msg = txt.encode("utf-8")
    client.sendall(msg)
    client.close()

def send_img():
    port = 50000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((cur_server, port))
    conn = client.makefile('wb')
    cam = cv2.VideoCapture(0)
    print("Image Taken")
    cam.set(3, 640);
    cam.set(4, 480);
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)
    print("{0}: {1}".format("Sending", size))
    client.sendall(struct.pack(">L", size) + data)
    cam.release()

def recv_txt():
    serv = socket.socket()
    host = socket.gethostname()
    port = 60000
    serv.bind((host,port))
    print("Waiting for connection at {0} Port: {1}".format(host, port))
    serv.listen(5)
    conn, client = serv.accept()
    print("Connected to {0} at Port: {1}".format(client[0], client[1]))
    msg = conn.recv(2048).decode()
    print("Message Recieved:", msg)
    conn.close()
    serv.close()
    return msg
