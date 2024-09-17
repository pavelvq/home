import json, os, importlib

class ConfigReader():
    def __init__(self, from_, develop=False, loadwebplugin=False):
        if develop:
            self.config = json.loads(open("config.json", 'r').read())
        else:
            for i in os.listdir('/home/'):
                if 'config.json' in os.listdir('/home/'+i):
                    self.config = json.loads(open('/home/'+i+'/config.json', 'r').read())
                    
        if from_ == "web":
            self.load_rndis_conf()
            self.load_web_conf()
            self.load_web_plugins()
            self.config["loaded_from"] = "web"
        elif from_ == "rndis":
            self.load_rndis_conf()
            self.load_web_conf()
            if loadwebplugin: self.load_web_plugins(onlyone=loadwebplugin, nocore=True)
            self.config["loaded_from"] = "rndismodule"
        
        
    def load_rndis_conf(self):
        self.config["rndis_"] = self.config["rndis"]
        temp_rndis = json.loads(open(self.config["workspace"]+"/"+self.config["rndis"], 'r').read())
        self.config["rndis"] = temp_rndis["rndis"]
        self.config["usbdrive"] = temp_rndis["usbdrive"]
        
    def load_web_conf(self):
        self.config["web_"] = self.config["web"]
        self.config["web"] = json.loads(open(self.config["workspace"]+"/"+self.config["web"], 'r').read())["web"]
        
        
    def load_web_plugins(self, onlyone=False, nocore=False):
        self.config["webplugins_"] = self.config["webplugins"]
        temp_plugins_path = self.config["webplugins"]
        self.config["plugins"] = {}
        for i in os.listdir(self.config["workspace"]+"/"+temp_plugins_path):
            try:
                self.config["plugins"][i] = json.loads(open(self.config["workspace"]+"/"+temp_plugins_path+"/"+i+"/config.json", 'r').read())[i]
                if self.config["plugins"][i]["enable"] and not onlyone:
                    if self.config["plugins"][i]["loadcore"] and not nocore:
                        self.config["plugins"][i]["core"] = importlib.import_module("plugins."+i)
                    if "web" in os.listdir(self.config["workspace"]+"/"+temp_plugins_path+"/"+i) and not nocore:
                        self.config["plugins"][i]["web"] = importlib.import_module("plugins."+i+".web")
                elif not i == onlyone:
                    del self.config["plugins"][i]
            except Exception as e:
                print(e)
                
def get_config_text(config):
    #remove cores
    for i in config["plugins"].keys():
        if "core" in config["plugins"][i].keys():
            del config["plugins"][i]["core"]
        if "web" in config["plugins"][i].keys():
            del config["plugins"][i]["web"]
            
    return json.dumps(config, indent=4)
    
def save(config):
    if type(config) is str:
        config = json.loads(config)
    else:
        for i in config["plugins"].keys():
            if "core" in config["plugins"][i].keys():
                del config["plugins"][i]["core"]
            if "web" in config["plugins"][i].keys():
                del config["plugins"][i]["core"]
    #rndis
    if "rndis" in config.keys():
        open(config["workspace"]+"/"+config["rndis_"], 'w').write(json.dumps({"rndis": config["rndis"], "usbdrive": config["usbdrive"]}, indent=4))
        del config["rndis"]
        del config["usbdrive"]
        config["rndis"] = config["rndis_"]
        del config["rndis_"]
        
    #web
    if "web" in config.keys():
        open(config["workspace"]+"/"+config["web_"], 'w').write(json.dumps({"web": config["web"]}, indent=4))
        del config["web"]
        config["web"] = config["web_"]
        del config["web_"]
        
    #plugins
    if config["loaded_from"] == "web":
        if "plugins" in config.keys():
            for i in os.listdir(config["workspace"]+"/"+config["webplugins_"]):
                if i in config["plugins"].keys():
                    open(config["workspace"]+"/"+config["webplugins_"]+"/"+i+"/config.json", 'w').write(json.dumps({i: config["plugins"][i]}, indent=4))
            del config["plugins"]
            config["webplugins"] = config["webplugins_"]
            del config["webplugins_"]
    
    del config["loaded_from"] 
    open(config["workspace"]+"/"+"config.json", 'w').write(json.dumps(config, indent=4))
    
def mywebplugin(name):
    tmpconf = ConfigReader(from_=name).config
    if name in os.listdir(tmpconf["workspace"]+"/"+tmpconf["webplugins"]):
        return tmpconf, json.loads(open(tmpconf["workspace"]+"/"+tmpconf["webplugins"]+"/"+name+"/"+"config.json", 'r').read())[name], tmpconf["workspace"]+"/"+tmpconf["webplugins"]+"/"+name
    else:
        return None, None, None
        
plpages = {}