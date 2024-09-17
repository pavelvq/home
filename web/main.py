import json, os, sys
import flask_login

from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from modules.config import ConfigReader, get_config_text, save, plpages
from modules import connectedpc
from modules.wifi import Wifi
from modules.notifications import MainNotificator, Notificator

config = ConfigReader(from_="web").config

#FLASK
app = Flask(__name__)
app.secret_key = config["web"]["secret_key"]

#MODULES, PLUGINS
connected = connectedpc.pc(config["rndis"]["ip"], config["plugins"]["connectedpc"], config["workspace"])
wifim = Wifi(config["db"])
nc = Notificator("main")
mnotificator = MainNotificator(config["db"])

#CONNECT NOTIFICATORS FOR MODULES
mnotificator.addNotificator(nc)
mnotificator.addNotificator(connected.nc)
mnotificator.addNotificator(wifim.nc)

for i in config["plugins"].keys():
    if "web" in config["plugins"][i].keys():
        try:
            app.register_blueprint(config["plugins"][i]["web"].blueprint)
            plpages[i] = config["plugins"][i]["web"].PAGES
        except:
            nc.error(f'failed to load "{i}" (plugin) web module')
            
        try:
            mnotificator.addNotificator(config["plugins"][i]["web"].notificator)
        except:
            nc.warn(f'failed to load "{i}" (plugin) notificator')

#loading error checking
if connected.errors:
    sys.exit()

#******************************AUTH******************************
#if you want, you can add a module for a database with users. Then it will be possible to change the password... etc.
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self, login, password):
        self.id = login
        self.password = password

def user_generator(login):
    try:
        return User(login, config["web"]["users"][login]["password"])
    except:
        flask_login.logout_user()

@login_manager.user_loader
def user_loader(login):
    return user_generator(login)
    
@app.get("/login")
def login():
    return render_template("login.html")
     
@app.post("/login")
def postlogin():
    if request.form["login"] in config["web"]["users"].keys():
        user = user_generator(request.form["login"])

        if user.password != request.form["password"]:
            return redirect(url_for("login"))

        flask_login.login_user(user, remember=True)
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))
     
@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("home"))
#******************************AUTH******************************

#***********************ERRORS***********************
@app.errorhandler(401)
def e401(e):
    return redirect(url_for("login"))

@app.errorhandler(404)
def e404(e):
    return render_template('errors/404.html')
    
@app.route("/notifications")
@flask_login.login_required
def notifications():
    args = request.args
    if args.get("request") == "last":
        return mnotificator.last()
    elif args.get("request") == "all":
        return json.dumps(mnotificator.bstorage.all())
    elif args.get("request") == "clear":
        mnotificator.bstorage.clean(flask_login.current_user.id)
        return "ok"
    else:
        return "error in request"
    
#***********************ERRORS***********************

#***********************HOME***********************
@app.route("/home")
@flask_login.login_required
def to_home():
    return redirect(url_for("home"))

@app.route("/")
@flask_login.login_required
def home():
    return render_template('home.html')
#***********************HOME***********************

#***********************PLUGINS***********************
@app.route("/plugins/")
@flask_login.login_required
def plugins():
    return render_template('modules/sidebar-plugins.html', plugins=plpages)
    
#***********************PLUGINS***********************

#***********************MODULE***********************
@app.route("/module/ssh")
@flask_login.login_required
def modulessh():
    if connected.server.connected():
        connected.open_ssh_to_home()
        return redirect(url_for("home"))
    else:
        return "ssh page"
    
    
@app.route("/module/settings")
@flask_login.login_required
def modulesettings():
    return render_template('module-settings.html', settings=get_config_text(config))
    
@app.route("/module/save", methods=['POST'])
@flask_login.login_required
def modulesettingssave():
    jsettings = request.form.get('settings')
    save(jsettings)
    return redirect(url_for("modulesettings"))
    
@app.route("/module/reloadfull", methods=['POST'])
@flask_login.login_required
def modulesettingsreload():
    jsettings = request.form.get('settings')
    save(jsettings)
    os.system("sudo reboot")
    

@app.route("/module/wifi")
@flask_login.login_required
def modulewifi():
    args = request.args
    if args.get("request") == None:
        return render_template('module-wifi.html', ifname=wifim.interface, 
                                                   connected=wifim.get_connected())
    elif args.get("request") == "standard":
        ssid = args.get("ssid")
        password = args.get("pass")
        if ssid == None or password == None: return "error in request"
        return "ok" if wifim.make_standard(ssid, password) else "error"
    elif args.get("request") == "rstandard":
        wifim.remove_standard()
        return "ok"
    elif args.get("request") == "connect":
        ssid = args.get("ssid")
        password = args.get("pass")
        if ssid == None or password == None: return "error in request"
        return "ok" if wifim.connect(ssid, password) else "error"
    elif args.get("request") == "disconnect":
        return "ok" if wifim.disconnect() else "error"
    elif args.get("request") == "getpass":
        ssid = args.get("ssid")
        if ssid == None: return "error in request"
        return wifim.get_pass(ssid)
    elif args.get("request") == "getconnected":
        return wifim.get_connected()
    else:
        return "error in request"
    
@app.route("/module/wifi/scan")
@flask_login.login_required
def modulewifiscan():
    return render_template('module-wifi-table.html', scan=wifim.scan(), connected=wifim.get_connected())

#***********************MODULE***********************


          
app.run(host="0.0.0.0", port=config["web"]["port"], debug=False, use_reloader=False)