import pymysql
from modules.dbprotect import errintype, erringet


class NGDB():
    def __init__(self, user, password, host='localhost', database='homeyedb'):
        self.connection = pymysql.connect(host=host, 
                                          user=user,
                                          password=password, 
                                          database=database)
        self.cursor = self.connection.cursor()
        self.nlinks_create_q = """CREATE TABLE `nlinks` (
    `id` INT NOT NULL AUTO_INCREMENT, 
    `name` VARCHAR(255), 
    `ip` VARCHAR(255), 
    `port` INT, 
    `nip` VARCHAR(255), 
    `nport` INT, 
    `token` VARCHAR(255), 
    `status` INT, 
    PRIMARY KEY (`id`));"""
        self.columns = ["id", "name", "ip", "port", "nip", "nport", "token", "status"]
        self.nlinks_insert_q = "INSERT INTO nlinks (name, ip, port, nip, nport, token, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.nlinks_insert_q_with_id = "INSERT INTO nlinks (id, name, ip, port, nip, nport, token, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.clean()
        
    def add_link(self, name, ip, port, nip, nport, token, status=True, id=False):
        if status:
            status = 1
        elif not status:
            status = 0
        elif status == 0 or status == 1:
            pass
            
        id = errintype(id, int)
        port = errintype(port, int)
        nport = errintype(nport, int)
        if id[0] or port[0] or nport[0]: return False

        if id:
            self.cursor.execute(self.nlinks_insert_q_with_id, (id[1], name, ip, port[1], nip, nport[1], token, status))
        else:
            self.cursor.execute(self.nlinks_insert_q, (name, ip, port[1], nip, nport[1], token, status))

        self.connection.commit()
        return True

    def all(self):
        self.cursor.execute("SELECT * FROM nlinks")
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
            if 'nlinks' in list_:
                self.cursor.execute("DROP TABLE nlinks")
        self.cursor.execute(self.nlinks_create_q)
        self.connection.commit()

    def disable_link(self, id):
        id = errintype(id, int)
        if id[0]: return False
        self.cursor.execute("UPDATE nlinks SET status=0 WHERE id=%s", (id[1]))
        self.connection.commit()
        return True
        
    def check_token(self, token):
        #True if token unique
        self.cursor.execute("SELECT * FROM nlinks WHERE token=%s", (token))
        try:
            self.cursor.fetchall()[0]
            return False
        except:
            return True
            
    def session_exists(self, ip, port):
        #True if token unique
        port = errintype(port, int)
        if port[0]: return False
        self.cursor.execute("SELECT * FROM nlinks WHERE ip=%s AND port=%s", (ip, port[1]))
        try:
            self.cursor.fetchall()[0]
            return True
        except:
            return False
    
    def update_link(self, id, newnip, newnport):
        id = errintype(id, int)
        newnport = errintype(newnport, int)
        if id[0] or newnport[0]: return False
        old = self.byid(id)
        if old == None: return False
        self.cursor.execute("DELETE FROM nlinks WHERE id=%s", (id[1]))
        self.add_link(old[1], old[2], old[3], newnip, newnport[1], old[6], id=id[1])
        return True
        
    def byid(self, id, get=["*"]):
        id = errintype(id, int)
        if id[0]: return None
        if erringet(get, self.columns): return None
        self.cursor.execute(f"SELECT {','.join(get)} FROM nlinks WHERE id=%s", (id[0]))
        try:
            return self.cursor.fetchall()[0]
        except:
            return None
        
    def links_count(self, status=None):
        if status == None:
            self.cursor.execute("SELECT COUNT(1) FROM nlinks;")
            return self.cursor.fetchall()[0][0]
        elif str(status) == '0':
            self.cursor.execute("SELECT COUNT(1) FROM nlinks WHERE status=0;")
            return self.cursor.fetchall()[0][0]
        elif str(status) == '1':
            self.cursor.execute("SELECT COUNT(1) FROM nlinks WHERE status=1;")
            return self.cursor.fetchall()[0][0]