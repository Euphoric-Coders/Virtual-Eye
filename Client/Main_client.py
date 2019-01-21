import glob
import time
import os

servers = {"HOME":"SAMISH",
           "SAMAY" : "DESKTOP-12OV957",
           "PRERAK":"DESKTOP-B3GC6VI",
           "SAM":"VKGLaptop",
           "DJ":"DESKTOP-7C1T3TI",
           "MONU":"DESKTOP-I0SS64C"}

cur_server = servers["HOME"]
os.chdir("Subfiles\\")    
files = glob.glob("*.py")

for fl in files:
    file = open(fl)
    script = file.read()
    exec(script)
    file.close()

run = True
while run:
    start = time.time()
    values = ""
    out, status = VoiceDetect(mic)
    print(out)
    if status == True:
        val, func = Commands(out)
        op = val
        if op =='assist':
            while True:
                send_txt(op)
                send_img()
                op = recv_txt()
                print(op)
                Output(op)
                ex = VoiceDetect(mic,'',4)
                if 'exit assist' in ex:
                    break

        elif op == "vis":
            send_txt("vis")
            send_img()
            op = recv_txt()
            values = eval(op)
            
        else:
            if func=='clf':
                send_txt(val)
                send_img()
                op = recv_txt()
            elif func=="":
                op=val
            elif func=="exit":
                op=val
                run = False
        if values =="":
            print(op)
            Output(op)
        else:
            for i in values:
                print(i)
                Output(i)
                
    end  = time.time()
    print('Time taken:',end - start)
    input()
