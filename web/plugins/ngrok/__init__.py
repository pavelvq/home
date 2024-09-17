from plugins.ngrok.dbm import NGDB
from plugins.ngrok.mngrok import NgrokModule2
#from modules.ngrok.pid import waitforclose

class ngrok():
    def __init__(self, module, db, workspace, mainport):
        self.module = module
        self.ng = NgrokModule2(token=self.module["token"])
        self.db = NGDB(db["user"], db["password"], host=db["host"], database=db["database"])
        self.main = self.create("Main", "localhost", mainport)

    def create(self, name, ip, port):
        #self.ng.kill(ip, port)
        #if not self.db.check_token(token):
        #    return False
        if self.db.session_exists(ip, port):
            return False
        link = self.ng.new(ip, port)
        self.db.add_link(name, ip, port, link[0], link[1], self.module["token"])
        return True

    def disable(self, id):
        if self.db.byid(id, get=['status'])[0] == 1:
            data = self.db.byid(id, get=['nip', 'nport'])
            self.ng.kill(data[0], data[1])
            #waitforclose(data[2])
            self.db.disable_link(id)

    def update(self, id):
        if self.db.byid(id, get=['status'])[0] == 1:
            data = self.db.byid(id, get=['nip', 'nport'])
            self.ng.kill(data[0], data[1])
            #waitforclose(data[2])
        data = self.db.byid(id, get=['ip', 'port'])
        link = self.ng.new(data[0], data[1])
        self.db.update_link(id, link[0], link[1])