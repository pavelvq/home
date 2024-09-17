import flask_login
from flask import Blueprint
from flask import render_template
from flask import request, redirect, url_for
from modules.config import mywebplugin
from modules.notifications import Notificator
from plugins import ngrok

PLUGIN = "ngrok"
VERSION = "1.0.0"
PAGES = {"icon": "mdi mdi-earth", "pages": [{"name": "Port Forwarder", "url": "/plugins/forwarder"}]}

mainconf, plconf, plpath = mywebplugin(PLUGIN)
forwarder = ngrok.ngrok(plconf, mainconf["db"], mainconf["workspace"], 3807)


#blueprint name (first arg) - plname_web 
blueprint = Blueprint('ngrok_web', __name__, template_folder=plpath+"/web/templates")
notificator = Notificator(PLUGIN)

#***********************forwarder plugin***********************
@blueprint.route("/plugins/forwarder")
@flask_login.login_required
def forwarderpage():
    try:
        working = forwarder.db.links_count(status=1)
        stopped = forwarder.db.links_count(status=0)
        total = forwarder.db.links_count()
        all = forwarder.db.all()
        return render_template('forwarder-plugin.html', working=working, 
                                             stopped=stopped, 
                                             total=total,
                                             all=all)
    except Exception as e:
        notificator.error("plguin error")
        notificator.error(str(e))
        return redirect(url_for("home"))
     
@blueprint.route("/plugins/forwarder/re", methods=['POST'])
@flask_login.login_required
def upldate_link():
    try:
        id = request.form.get("id")
        forwarder.update(id)
        return redirect(url_for("ngrok_web.forwarderpage"))
    except Exception as e:
        notificator.error("plguin error")
        notificator.error(str(e))
        return redirect(url_for("ngrok_web.forwarderpage"))

@blueprint.route("/plugins/forwarder/dis", methods=['POST'])
def disabe_link():
    try:
        id = request.form.get("id")
        forwarder.disable(id)
        return redirect(url_for("ngrok_web.forwarderpage"))
    except Exception as e:
        notificator.error("plguin error")
        notificator.error(str(e))
        return redirect(url_for("ngrok_web.forwarderpage"))
     
@blueprint.route("/plugins/forwarder/create", methods=['POST'])
def create_link():
    try:
        name = request.form.get("name")
        ip = request.form.get("ip")
        port = str(request.form.get("port"))
        forwarder.create(name, ip, port)
        notificator.info(f"forwarded port for {ip}:{port}")
        return redirect(url_for("ngrok_web.forwarderpage"))
    except Exception as e:
        notificator.error("plguin error")
        notificator.error(str(e))
        return redirect(url_for("ngrok_web.forwarderpage"))
     
#**************************************************************