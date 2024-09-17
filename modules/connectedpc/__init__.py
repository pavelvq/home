import json
import socket
import threading
import time
from modules.notifications import Notificator


global connect_
connect_ = None


def listener(server, ip, port, nc):
    global connect_
    print(" * waiting for usb pc connection...")
    while True:
        try:
            server.bind((ip, int(port)))
            break
        except Exception as e:
            print(e)
            time.sleep(5)
    print(" * homeye connected via usb")
    print(" * waiting app...")
    server.listen(1)
    connect_ = server.accept()
    print(" * connected!")
    nc.info("homeye module connected to pc!")
    

class server():
    connection = None
    address = None
    
    def __init__(self, ip, port, nc):
        self.nc = nc
        self.server = socket.socket()
        self.listener = threading.Thread(target=listener, args=(self.server, ip, port, self.nc,))
        self.listener.start()
        
    def send(self, jmsg):
        if not self.connected(): return
        self.connection.send(json.dumps(jmsg).encode())
        
    def recv(self):
        if not self.connected(): return
        buffer = ''
        while True:
            jmsg = self.connection.recv(512)
            buffer += jmsg.decode()
            if buffer[-1] == '}':
                return json.loads(buffer)
                
    def connected(self):
        global connect_
        if connect_ == None:
            return False
        else:
            if self.connection == None:
                self.connection, self.address = connect_
            return True
        

class pc():
    def __init__(self, ip, config, workspace):
        self.nc = Notificator("usb")
        self.server = server(ip, config["port"], self.nc)
        self.ssh_home = config["ssh_home"]
        self.errors = False
        self.errdict = json.loads(open(workspace+config["errordict"], 'r').read())
        
    def error(self, errid):
        self.server.send({'type': 'error', 'errid': errid, 'msg': self.errdict[str(errid)]})
        self.nc.warn(self.errdict[str(errid)])
        self.errors = True
        
    def openssh(self, ip, port, user, password):
        self.server.send({'type': 'ssh', 'ip': ip, 'port': port, 'user': user, 'password': password})
        
    def open_ssh_to_home(self):
        self.openssh(self.ssh_home["ip"], self.ssh_home["port"], self.ssh_home["username"], self.ssh_home["password"])
        
        
class pc_for_develop():
    def __init__(self, ip, config, workspace):
        self.errors = False
        
    def error(self, errid):
        pass
        
    def openssh(self, ip, port, user, password):
        pass
        
    def open_ssh_to_home(self):
        pass