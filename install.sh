#!/bin/bash
SCRIPTPATH=$(dirname $(readlink -f "$0"))
if [ $(id -u) -eq 0 ]
    then echo " * No need to run as root!"
    exit
fi

clear

if [[ "$COLUMNS" -ge "103" ]]; then
    echo "      ___                    ___                    ___                    ___        * HOME           "
    echo "     /\__\                  /\  \                  /\__\                  /\  \       * OBSERVE &      "
    echo "    /:/  /                 /::\  \                /::|  |                /::\  \      * MONITORING     "
    echo "   /:/__/                 /:/\:\  \              /:|:|  |               /:/\:\  \     * ENVIRONMENT    "
    echo "  /::\  \ ___            /:/  \:\  \            /:/|:|__|__            /::\~\:\  \                     "
    echo " /:/\:\  /\__\          /:/__/ \:\__\          /:/ |::::\__\          /:/\:\ \:\__\                    "
    echo " \/__\:\/:/  /          \:\  \ /:/  /          \/__/~~/:/  /          \:\~\:\ \/__/                    "
    echo "      \::/  /            \:\  /:/  /                 /:/  /            \:\ \:\__\                      "
    echo "      /:/  /              \:\/:/  /                 /:/  /              \:\ \/__/                      "
    echo "     /:/  /                \::/  /                 /:/  /                \:\__\                        "
    echo "     \/__/                  \/__/                  \/__/                  \/__/       | installation..."
    echo "                                                                                                       "
else
    echo '"HOME" installation...'
fi


if [[ "$COLUMNS" -ge "103" ]]; then
    echo "-------------------------------------------- main settings --------------------------------------------"
fi

read -p "Username (OS): " username
if [[ "$username" == "" ]]; then
    echo " * Username (OS) is required!"
    exit
fi

read -p "Password (OS): " password
if [[ "$password" == "" ]]; then
    echo " * Password (OS) is required!"
    exit
fi

read -p "Install to (default /home/$username/): " installpath
if [[ "$installpath" == "" ]]; then
    installpath="/home/$username"
fi


if [[ "$COLUMNS" -ge "103" ]]; then
    echo "------------------------------------------------- WEB -------------------------------------------------"
fi

read -p "Install web? (y/n): " needweb
if [[ "$needweb" == "y" ]]; then
    needweb=true
    read -p " + Username (WEB): " webusername
    if [[ "$webusername" == "" ]]; then
        echo " * Username (WEB) is required!"
        exit
    fi

    read -p " + Password (WEB): " webpassword
    if [[ "$webpassword" == "" ]]; then
        echo " * Password (WEB) is required!"
        exit
    fi

    read -p " + Install web-api? (y/n): " needwebapi
    if [[ "$needwebapi" == "y" ]]; then
        needwebapi=true
    else
        needwebapi=false
    fi
else
    needweb=false
fi

echo
read -p "The installation will affect many system settings. Сontinue? (y/n): " go
if [[ "$go" -ne "y" ]]; then
    exit
fi

clear
echo " * Updating system..."
sudo apt-get -y update
sudo apt-get -y upgrade

#PYTHON
echo " * Installing python3..."
sudo apt-get -y install python3
sudo apt-get -y install python3-pip
python3 -m pip install -r $SCRIPTPATH/assets/pyrequirements.txt

#CPP
echo " * Installing cpp-dependencies..."
sudo apt-get -y install cmake
sudo apt-get -y install build-essential gdb
sudo apt-get -y install mingw-w64

#MYSQL
echo " * Installing mariadb..."
sudo apt-get -y install mariadb-server

#chmod -R ugo+rw /etc/wpa_supplicant/
#https://www.chilkatsoft.com/downloads_clion.asp