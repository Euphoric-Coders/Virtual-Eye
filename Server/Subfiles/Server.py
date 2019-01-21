import socket, pickle, cv2, zlib, struct, select
import numpy as np

def recv_txt():
    serv = socket.socket()
    host = socket.gethostname()
    port = 60000
    serv.bind((host,port))
    print("Waiting for connection at {0} Port: {1}".format(host, port))
    serv.listen(5)
    conn, client = serv.accept()
    print("Connected to {0} at Port: {1}".format(client[0], client[1]))
    msg = conn.recv(1024).decode()
    print("Message Recieved:", msg)
    conn.close()
    serv.close()
    return msg

def send_txt(txt = ""):
    txt = str(txt)
    client = socket.socket()
    host = cur_server
    port = 60000
    client.connect((host,port))
    print("Connected to {0} at port: {1}".format(host,port))
    msg = txt.encode("utf-8")
    client.sendall(msg)
    print("Connection closed")
    client.close()

def recv_img():
    serv = socket.socket()
    host = socket.gethostname()
    port = 50000
    serv.bind((host,port))
    print("Waiting for connection at {0} Port: {1}".format(host, port))
    serv.listen(5)
    conn, client = serv.accept()
    print("Connected to {0} at Port: {1}".format(client[0], client[1]))
    data = b""
    size = struct.calcsize(">L")
    print("Size: {0}".format(size))

    while len(data) < size:
        print("Recieving: {0}".format(len(data)))
        data += conn.recv(4096)

    print("Image recieved")
    arch_size = data[:size]
    data = data[size:]
    msg_size = struct.unpack(">L", arch_size)[0]
    print("Message size: {0}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)

    fm_data = data[:msg_size]
    data = data[msg_size:]
    fm = pickle.loads(fm_data, fix_imports=True, encoding="bytes")
    fm = cv2.imdecode(fm, cv2.IMREAD_COLOR)
    output_file = "imgnew.jpg"
    cv2.imwrite(output_file, fm)
    conn.close()
    serv.close()
    print("Connection closed")
    return "img.jpg"
