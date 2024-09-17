import pywifi
import hashlib, binascii
import time, subprocess, os
from modules.wifi.dbm import WifiDB
from modules.notifications import Notificator

class Wifi():
    connected_to = None
    
    def __init__(self, db, interface="wlan0"):
        self.interface = interface
        self.db = WifiDB(db["user"], db["password"], host=db["host"], database=db["database"])
        self.wifim = pywifi.PyWiFi()
        self.iface = [i for i in self.wifim.interfaces() if i.name() == interface][0]
        self.wpa_conf = "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\n\n"
        self.nc = Notificator("wifi")
        self.get_standard()
        
    def wpa_psk(self, ssid, password):
        dk = hashlib.pbkdf2_hmac(
            'sha1',
            str.encode(password),
            str.encode(ssid),
            4096,
            256
        )
        return (binascii.hexlify(dk)[0:64].decode('utf8'))
        
    def scan(self, t=2):
        self.iface.scan()
        time.sleep(t)
        scanr = self.iface.scan_results()
        v, inv = self.db.process(scanr, findby=self.interface)
        return [self.db.get_standard()], v, inv
        
    def make_standard(self, ssid, password):
        try:
            netconf = f'network={{\n\tssid="{ssid}"\n\tpsk={self.wpa_psk(ssid, password)}\n}}\n'
            #if not os.geteuid() == 0:
            #    open("tmp_wifi_conf", "w").write(self.wpa_conf+netconf)
            #    os.system("sudo mv tmp_wifi_conf /etc/wpa_supplicant/wpa_supplicant.conf")
            #else:
            open("/etc/wpa_supplicant/wpa_supplicant.conf", "w").write(self.wpa_conf+netconf)
            self.db.make_standard(ssid)
            return True
        except Exception as e:
            self.nc.error(str(e))
            return False
            
    def remove_standard(self):
        try:
            #if not os.geteuid() == 0:
            #    open("tmp_wifi_conf", "w").write(self.wpa_conf)
            #    os.system("sudo mv tmp_wifi_conf /etc/wpa_supplicant/wpa_supplicant.conf")
            #else:
            open("/etc/wpa_supplicant/wpa_supplicant.conf", "w").write(self.wpa_conf)
            self.db.remove_standard()
            return True
        except Exception as e:
            self.nc.error(str(e))
            return False
        
    def get_connected(self):
        out = subprocess.check_output(["/bin/bash", "-c", "iwconfig", "|", "grep", "wlan0"]).decode("utf-8")
        if "off/any" in out: return "None"
        _, g, n = "", False, ""
        for i in out:
            if g:
                n += i
                if n[0] == '"' and n[-1] == '"' and not len(n) == 1:
                    break
            else:
                _ += i
                if _[-6:] == "ESSID:":
                    g = True
        self.connected_to = n.replace('"', '').replace(' ', '')
        return self.connected_to
        
    def get_standard(self):
        #if not os.geteuid() == 0:
        #    out = subprocess.check_output(["/bin/bash", "-c", "sudo", "cat", "/etc/wpa_supplicant/wpa_supplicant.conf"]).decode("utf-8")
        #else:
        out = open("/etc/wpa_supplicant/wpa_supplicant.conf", "r").read()
            
        if not "ssid" in out: 
            self.db.remove_standard()
            return None
        _, g, n = "", False, ""
        for i in out:
            if g:
                n += i
                if n[0] == '"' and n[-1] == '"' and not len(n) == 1:
                    break
            else:
                _ += i
                if _[-5:] == "ssid=":
                    g = True
        n = n.replace('"', '').replace(' ', '')
        self.db.make_standard(n)
        return n
        
    def get_pass(self, ssid):
        password = self.db.get_pass(ssid)
        return "" if password == None else password
        
    def connect(self, ssid, password):
        self.iface.connect(self.generate_profile(ssid, password))
        for i in range(10):
            time.sleep(0.5)
            if self.iface.status() == pywifi.const.IFACE_CONNECTED:
                self.db.add_password(ssid, password)
                self.nc.info(f"interface connected to {ssid}")
                return True
        return False
        
    def disconnect(self):
        self.iface.disconnect()
        for i in range(10):
            time.sleep(0.5)
            if self.iface.status() in [pywifi.const.IFACE_DISCONNECTED, pywifi.const.IFACE_INACTIVE]:
                self.nc.info("interface disconnected")
                return True
        return False

    def generate_profile(self, ssid, password):
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.key = password
        return profile
       
    def ifconfig(self, interface):
        return subprocess.check_output(["/bin/bash", "-c", "ifconfig", interface]).decode("utf-8")
        