from modules.wifi import Wifi

a = Wifi({
        "user": "root",
        "password": "Wasdx3556",
        "host": "localhost",
        "database": "homeyedb"
    })
    
print(a.get_connected())
#a.db.add_wifi_commit("MAD", "DFSBSGGSDGSDG", "fdsdfsdfsdf", 0, "wlan0")
#a.db.process(a.scan(), findby="wlan0")
#print(a.scan())