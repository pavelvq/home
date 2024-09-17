import pymysql
from modules.dbprotect import errintype


class NotificationDB():
    def __init__(self, user, password, host='localhost', database='homeyedb'):
        self.connection = pymysql.connect(host=host, 
                                          user=user,
                                          password=password, 
                                          database=database)
        self.cursor = self.connection.cursor()
        self.nc_create_q = """CREATE TABLE IF NOT EXISTS `notifications` (
    `userid` VARCHAR(255), 
    `getfrom` VARCHAR(255), 
    `type` VARCHAR(255), 
    `message` VARCHAR(255), 
    `time` INT);"""
        self.nc_insert_q = "INSERT INTO notifications (userid, getfrom, type, message, time) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(self.nc_create_q)
        self.connection.commit()
           
    def add(self, userid, getfrom, type, message, time):
        time = errintype(time, int)
        if time[0]: return False
        self.cursor.execute(self.nc_insert_q, (userid, getfrom, type, message, time[1]))
        self.connection.commit()
        return True

    def all(self, userid):
        self.cursor.execute("SELECT getfrom, type, message, time FROM notifications WHERE userid=%s", (userid))
        try:
            return self.cursor.fetchall()
        except:
            return []
    
    def clean(self, userid):
        self.cursor.execute("DELETE FROM notifications WHERE userid=%s", (userid))
        self.connection.commit()