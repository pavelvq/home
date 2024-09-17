import pymysql
from modules.dbprotect import errintype


class WifiDB():
    def __init__(self, user, password, host='localhost', database='homeyedb'):
        self.connection = pymysql.connect(host=host, 
                                          user=user,
                                          password=password, 
                                          database=database)
        self.cursor = self.connection.cursor()
        self.wifilist_create_q = """CREATE TABLE IF NOT EXISTS `wifilist` (
    `id` INT NOT NULL AUTO_INCREMENT, 
    `ssid` VARCHAR(255), 
    `bssid` VARCHAR(255), 
    `password` VARCHAR(255), 
    `standard` INT, 
    `findby` VARCHAR(255),
    PRIMARY KEY (`id`));"""
        self.wifilist_insert_q = "INSERT INTO wifilist (ssid, bssid, password, standard, findby) VALUES (%s, %s, %s, %s, %s)"
        self.wifilist_sinsert_q = "INSERT INTO wifilist (ssid, bssid, standard, findby) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(self.wifilist_create_q)
        self.connection.commit()
        
    def add_wifi(self, ssid, bssid, password, standard, findby):
        standard = errintype(standard, int)
        if standard[0]: return False
        self.cursor.execute(self.wifilist_insert_q, (ssid, bssid, password, standard[1], findby))
        return True
    
    def add_wifi_commit(self, ssid, bssid, password, standard, findby):
        standard = errintype(standard, int)
        if standard[0]: return False
        self.cursor.execute(self.wifilist_insert_q, (ssid, bssid, password, standard[1], findby))
        self.connection.commit()
        return True
        
    def add_wifi_scan(self, ssid, bssid, standard, findby):
        standard = errintype(standard, int)
        if standard[0]: return [ssid, bssid, None, standard, findby]
        self.cursor.execute(self.wifilist_sinsert_q, (ssid, bssid, standard[1], findby))
        return [ssid, bssid, None, int(standard), findby]
        
    def add_wifi_scan_commit(self, ssid, bssid, standard, findby):
        standard = errintype(standard, int)
        if standard[0]: return [ssid, bssid, None, standard, findby]
        self.cursor.execute(self.wifilist_sinsert_q, (ssid, bssid, standard[1], findby))
        self.connection.commit()
        return [ssid, bssid, None, int(standard), findby]

    def all(self):
        self.cursor.execute("SELECT ssid, bssid, password, standard, findby, id FROM wifilist")
        try:
            return self.cursor.fetchall()
        except:
            return []
            
    def all_old_format(self):
        self.cursor.execute("SELECT * FROM wifilist")
        try:
            return self.cursor.fetchall()
        except:
            return []

    def tables(self):
        self.cursor.execute("SHOW TABLES")
        try:
            return self.cursor.fetchall()[0]
        except:
            return None
    
    def clean(self):
        list_ = self.tables()
        if list_ != None:
            if 'wifilist' in list_:
                self.cursor.execute("DROP TABLE wifilist")
        self.cursor.execute(self.wifilist_create_q)
        self.connection.commit()

    def process(self, scan_result, findby="wlan0"):
        active, noactive, all_ = [], [], self.all()
        wifidict = {i[0]: i[-1] for i in all_}
        for i in scan_result:
            if not i.ssid in wifidict.keys():
                _ = self.add_wifi_scan(i.ssid, i.bssid, 0, findby)
                active.append(_)
            else:
                self.cursor.execute("UPDATE wifilist SET bssid=%s, findby=%s WHERE ssid=%s", (i.bssid, findby, i.ssid))
                active.append(self.byssid(i.ssid))
                
        for i in all_:
            if not i[0] in [d[0] for d in active]:
                noactive.append(i)
        self.connection.commit()
                
        return active, noactive
                    
    def byssid(self, ssid):
        self.cursor.execute("SELECT ssid, bssid, password, standard, findby, id FROM wifilist WHERE ssid=%s", (ssid))
        try:
            return self.cursor.fetchone()
        except:
            return []
        
    def get_standard(self):
        self.cursor.execute("SELECT ssid, bssid, password, standard, findby, id FROM wifilist WHERE standard=1")
        try:
            return self.cursor.fetchall()[0]
        except:
            return []
            
    def get_pass(self, ssid):
        self.cursor.execute("SELECT password FROM wifilist WHERE ssid=%s", (ssid))
        try:
            return self.cursor.fetchone()[0]
        except:
            return None
            
    def exists(self, dbout):
        try:
            _ = dbout[0]
            return True
        except:
            return False

    def make_standard(self, ssid):
        if self.exists(self.byssid(ssid)):
            self.cursor.execute("UPDATE wifilist SET standard=0 WHERE standard=1")
            self.cursor.execute("UPDATE wifilist SET standard=1 WHERE ssid=%s", (ssid))
        else:
            self.cursor.execute("INSERT INTO wifilist (ssid, standard) VALUES (%s, 1)", (ssid))
        self.connection.commit()
        
    def remove_standard(self):
        self.cursor.execute("UPDATE wifilist SET standard=0 WHERE standard=1")
        self.connection.commit()
        
    def add_password(self, ssid, password):
        if self.exists(self.byssid(ssid)):
            self.cursor.execute("UPDATE wifilist SET password=%s WHERE ssid=%s", (password, ssid))
        else:
            self.cursor.execute("INSERT INTO wifilist (ssid, password) VALUES (%s, %s)", (ssid, password))
        self.connection.commit()