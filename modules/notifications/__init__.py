import time, json
import flask_login
#from modules.notifications.dbm import NotificationDB

class Notificator():
    storage = {}

    def __init__(self, name):
        self.name = name
        
    def last(self, userid): 
        if not userid in self.storage.keys(): 
            if "tmp" in self.storage.keys(): 
                self.storage[userid] = self.storage["tmp"]
                del self.storage["tmp"]
            else:
                return None
        userstorage = self.storage[userid]
        if len(userstorage) > 0:
            _ = userstorage[0]
            self.storage[userid] = userstorage[1:]
            return _
        else:
            return None
            
    def error(self, message):
        userid = flask_login.current_user
        if userid == None:
            userid = "tmp"
        else:
            userid = userid.id
        if not userid in self.storage.keys(): self.storage[userid] = []
        self.storage[userid].append({'type': 'error', 'from': self.name, 'message': message, 'time': int(time.time())})
        
    def warn(self, message):
        userid = flask_login.current_user
        if userid == None:
            userid = "tmp"
        else:
            userid = userid.id
        if not userid in self.storage.keys(): self.storage[userid] = []
        self.storage[userid].append({'type': 'warn', 'from': self.name, 'message': message, 'time': int(time.time())})
       
    def info(self, message):
        userid = flask_login.current_user
        if userid == None:
            userid = "tmp"
        else:
            userid = userid.id
        if not userid in self.storage.keys(): self.storage[userid] = []
        self.storage[userid].append({'type': 'info', 'from': self.name, 'message': message, 'time': int(time.time())})
       
        
class MainNotificator():
    notificators = []
    storage = {}
    
    def __init__(self, db):
        pass
        #self.bstorage = NotificationDB(db["user"], db["password"], host=db["host"], database=db["database"])

    def addNotificator(self, notificator):
        self.notificators.append(notificator)
    
    def last(self):
        user = flask_login.current_user.id
        if not user in self.storage.keys():
            n = [i.last(user) for i in self.notificators]
            n = [i for i in n if not i == None]
            if len(n) == 0: return ""
            self.storage[user] = {i["time"]: i for i in n}
        if len(self.storage[user]) == 0:
            n = [i.last(user) for i in self.notificators]
            n = [i for i in n if not i == None]
            if len(n) == 0: return ""
            self.storage[user] = {i["time"]: i for i in n}
        key_ = min(self.storage[user], key=self.storage[user].get)
        _ = self.storage[user][key_]
        del self.storage[user][key_]
        #self.bstorage.add(user, _["from"], _["type"], _["message"], _["time"])
        return json.dumps(_)