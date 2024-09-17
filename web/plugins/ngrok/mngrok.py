#from pyngrok import ngrok
import ngrok
import subprocess
import socket


#someday I will make it possible to use infinity tokens
class NgrokModule():
    def __init__(self, host='localhost', port=6502, python='python', passm='./modules/'):  
        self.host = host
        self.port = port
        self.python = python
        self.passtng = passm+'/tngrok.py'
        self.passm = passm

    def kill(self, ip, port):
        open(self.passm+'/kills.list', 'w').write(open(self.passm+'/kills.list', 'r').read()+'\n'+ip+':'+str(port))

    def new(self, ip, port, token):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, int(self.port)))
        self.socket.listen()
        print([self.python, self.passtng, ip, str(port), token, 
                                 self.host, str(self.port), self.passm])
        proc = subprocess.Popen([self.python, self.passtng, ip, str(port), token, 
                                 self.host, str(self.port), self.passm], 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        conn, addr = self.socket.accept()
        out = conn.recv(1024).decode().split(':')+[proc.pid]
        conn.close()
        return out #[ip, port, pid]
    
#a = NgrokModule(passm='./modules/ngrok')
#d = a.new('localhost', 100, '1lteQKuJOryUGgUFInutT3FnYBU_4ABVj1L21LM64nsMQB6Pa')
#print(d)
#print(a.new('localhost', 110, '1lteQKuJOryUGgUFInutT3FnYBU_4ABVj1L21LM64nsMQB6Pa'))
#a.kill(d[0], d[1])

class NgrokModule2():
    def __init__(self, token):  
        self.token = token

    def kill(self, ip, port):
        ngrok.disconnect('tcp://'+ip+":"+str(port))

    def new(self, ip, port):
        print(f' * Creating ngrok session {ip}:{port}')
        connect = ngrok.forward(ip+":"+str(port), "tcp", authtoken=self.token)
        return str(connect.url())[6:].split(':') #[ip, port]