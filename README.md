# PwnLnX
An advanced **multi-threaded**, **multi-client** python reverse shell for hacking linux systems. There's still more work to do so feel free to help out with the development.
**Disclaimer**: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.

:mailbox: Reach me out!

[![Twitter Badge](https://img.shields.io/badge/-@spectertraw-1ca0f1?style=flat&labelColor=1ca0f1&logo=twitter&logoColor=white&link=https://twitter.com/spectertraww)](https://twitter.com/spectertraw) [![Mail Badge](https://img.shields.io/badge/-NOOBSEC-e74c3c?style=flat&labelColor=e74c3c&logo=youtube&logoColor=white)](https://youtube.com/noobsec) [![Mail Badge](https://img.shields.io/badge/-LevelivSecurity-e74c3c?style=flat&labelColor=e74c3c&logo=youtube&logoColor=white)](https://youtube.com/levelivsec) [![Mail Badge](https://img.shields.io/badge/-@spectertraww-e84393?style=flat&labelColor=e84393&logo=instagram&logoColor=white)](https://instagram.com/spectertraww) [![Mail Badge](https://img.shields.io/badge/-spectertraww-c0392b?style=flat&labelColor=c0392b&logo=gmail&logoColor=white)](mailto:spectertraww@gmail.com)

#### Communities 🕵🕵
##### Hang out with Level iv Security and Noob Security family on Discord.

 [![Discord](https://img.shields.io/discord/731263849990193153?color=red&label=@levelivsec&logo=Discord&style=flat-square&link=https://discord.gg/THJX876)](https://discord.gg/THJX876) [![Discord](https://img.shields.io/discord/805879201961607178?color=green&label=@NOOBSEC&logo=Discord&style=flat-square&link=https://discord.gg/wauq8bDbw4)](https://discord.gg/wauq8bDbw4)


## Getting Started
Please follow these instructions to get a copy of PwnLnX running on your local machine without any problems.
### Prerequisites
* Python3:
    * vidstream
    * pyfiglet
    * tqdm
    * mss
    * pyautogui
    * pyinstaller*
    * pip3

### Installing
```bash
# Download source code
git clone https://github.com/spectertraww/PwnLnX.git


cd PwnLnX

# download and  install the dipendences
chmod +x setup.sh

./setup.sh

```

### Getting PwnLnx up and running
#### Show help
`python3 PwnLnX.py --help`

#### Listening for incoming connections
`python3 PwnLnX.py --lhost [your localhost ip address] --lport [free port for listening incoming connections]`

#### creating a payload
```bash
chmod +x PwnGen.sh

./PwnGen.sh

```

>then follow the procedure to successifully create your payload, the payload is saved in PwnLnx directory. Send the created payload to victim

### PwnLnx Usage

| Command       | Usage                                                 |
| ------------- |-------------------------------------------------------| 
<<<<<<< HEAD
| help          | show help.     									    | 
=======
| help          | show help     									    | 
>>>>>>> 9bdb801d8a87810366c9e8eaa627173c200bf8b1
| exit          | close all the sessions and quit the progaram.         |
| show sessions | show all available sessions from connected.           |
| session [ID]  | interact with a specified session ID.                 | 
| kill [all/ID] | kill a specified session or all to kill all sessions. |
| banner        | have funny by changing the program banner             |

<<<<<<< HEAD
---

### Interact with a session

| Command            | Usage                                                   |
| -------------------|---------------------------------------------------------| 
| help               | show help.     									       | 
| quit               | close the current session.                              |
| background         | background the current session.                         |
| sysinfo            | get minimum target system information.                  | 
| create_persist     | create a persistant backdoor.                           |
| upload             | upload the specified filename to the target system.     |
| download           | download the specified filename from the target system. |
| screenshot         | take a desktop screenshot of the target system.         |
| start_screenshare  | start desktop screensharing.                            | 
| stop_screenshare   | stop desktop screensharing.                             |
| start_keycap       | start capturing victim's pressed keystrokes.            |
| dump_keycap        | dump/get the captured keystrokes.                       |
| stop_keycap		 | stop the capturing keystrokes.                          |

> **NB.** you can also execute linux system commands besides those listed above.
=======

>>>>>>> 9bdb801d8a87810366c9e8eaa627173c200bf8b1


