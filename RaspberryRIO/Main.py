
import sys, os, time, json, threading

import socket

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '//src')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '//Base_Modules')

import NetworkTable
import GamepadDevice

try:
	import robot
except Exception as error:
	print("============================================")
	print("ROBOT BUILD - BUILD FAILED")
	print(error)
	print("============================================")
	sys.exit()


# Creating socket server
print("Creating socket . . .")
server_socket = socket.socket(socket.SOCK_DGRAM)

socket_ip = 'localhost'
socket_port = 5599

try:
	server_socket.bind((socket_ip, socket_port))
except socket.error as msg:
	print("Bind failed. Error Code: " + str(msg[0]) + " Message: " + msg[1])
	sys.exit()

server_socket.listen(1)

print("Server waiting for client on " + str(socket_ip) + ":" + str(socket_port))

piBot = robot.Robot()

class methodThreadCall(threading.Thread):

	def __init__(self, threadName, methodReference):
		threading.Thread.__init__(self)
		self.threadName = threadName
		self.methodReference = methodReference


	def run(self):
		self.methodReference()



while True:
	# Waiting for a connection . . .
	print("Waiting for client connection . . .")
	client_socket, client_address = server_socket.accept()

	try :
		print("Connection from ", client_address)

		while (client_socket):

			## Incoming Data
			dataString = client_socket.recv(1024)
				## recvfrom also returns the address as a second parameter so you can distinguish between multiple connections
				## However the server_socket is only listening for (1) connection.

			if (dataString):

				print("Received Data", dataString)

				if (dataString and dataString.decode()[0] == "{"):

					data = json.loads(dataString.decode())

					if not ("type" in data):
						break

					try:
						if (data["type"] == "State"):
							if (data["data"] == "Enable"):
								piBot.robotInit()
								piBot._enable()
								methodThreadCall("operatorControlThread", piBot.operatorControl).start()
							elif (data["data"] == "Disable"):
								piBot.disable()
								piBot._disable()
						elif (data["type"] == "ControllerData"):
							NetworkTable.networkTable["_controllerData"] = data["data"]
							print(NetworkTable.networkTable["_controllerData"])
					except Exception as error:
						print("An error occured, ", error)

				else:
					print("Data not in payload form")

			else:
				print("No data from ", client_address)

			## Outgoing Data
			client_socket.send(json.dumps({"type" : "RobotStatusUpdate", "data": piBot._getStates()}).encode())

	except Exception as error:
		print("Issue with connection from client.", error)

	finally:
		print("Connection with client was terminated.")

		print("----------------------------")

		try:
			piBot.disable()
		except Exception as error:
			print("WARN: Failed to call disable() on Robot", error)

		try:
			piBot._disable()
		except Exception as error:
			print("SERIOUS: Failed to call _disable() on Robot", error)

		try:
			client_socket.close()
		except Exception as error:
			print("WARN: Failed to properly close socket.", error)

		print("----------------------------")
	

# py C:/_PROJECTS/RaspberryRIO/RaspberryRIO/Main.py

# REFERENCES

# https://github.com/adafruit/Adafruit_Python_PCA9685/blob/master/examples/simpletest.py
# https://www.raspberrypi.org/forums/viewtopic.php?t=205197