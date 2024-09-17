#!bin/python3
import os, sys
print(os.environ["PATH"])
import time
import json
import socket
from modules.config import ConfigReader, save

config = ConfigReader(from_="rndis", loadwebplugin="connectedpc").config
        
if not config["rndis"]["load_module"]:
    ###########################################
    vid=config["rndis"]["idVendor"]
    pid=config["rndis"]["idProduct"]
    imanfac=config["rndis"]["iManufacturer"]
    iprod=config["rndis"]["iProduct"]
    isn=config["rndis"]["iSerialNumber"]
    ###########################################

    ###########################################
    path_to_vdrive = config["workspace"]+config["usbdrive"]["path_to_vdrive"]
    mount_dir = config["usbdrive"]["mount_dir"]
    ###########################################

    stop_mass_storage = 'modprobe g_multi -r'
    start_rndis = f'modprobe g_multi file={path_to_vdrive} idVendor={vid} idProduct={pid} iManufacturer=\"{imanfac}\" iProduct=\"{iprod}\" iSerialNumber=\"{isn}\"'
    start_mass_storage = f'modprobe g_multi file={path_to_vdrive} removable=1 ro=0 stall=0 iManufacturer=\"{imanfac}\" iProduct=\"{iprod}\" iSerialNumber=\"{isn}\"'
    mount = f'mount -o loop {path_to_vdrive} {mount_dir}'
    umount = f'umount {mount_dir}'
    ifconfig = f'ifconfig {config["rndis"]["interface"]} {config["rndis"]["ip"]} netmask {config["rndis"]["netmask"]}'

    os.system(stop_mass_storage)
    os.system(start_mass_storage)

    while True:
        os.system(mount)
        if os.path.exists(mount_dir+'/.run'):
            os.remove(mount_dir+'/.run')
            os.system(stop_mass_storage)
            os.system(umount)
            os.system(start_rndis)
            break
        os.system(umount)
        time.sleep(10)

    os.system(ifconfig)

    server = socket.socket()
    server.bind((config["rndis"]["ip"], int(config["rndis"]["port"])))

    server.listen(1)
    conn, address = server.accept()
    conn.send((str(config["rndis"]["ip"]) + " " + str(config["rndis"]["ipv2"]) + " " + str(config["web"]["port"]) + " " + str(config["plugins"]["connectedpc"]["port"]) + " " + str(config["web"]["hostloader"])).encode())
    conn.close()
elif config["rndis"]["module"] == "hid_connect":
    #do something
    
    config["rndis"]["load_module"] = False
    save(config)
