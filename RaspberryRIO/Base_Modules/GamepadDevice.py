import NetworkTable

class DeviceInterface:

	_port = None
	axisDeadZone = 0.06

	def __init__(self, port):
		self._port = port

	def getDeviceDataFromTable(self):

		if not ("_controllerData" in NetworkTable.networkTable):
			# raise Exception("Could not find _controllerData in NetworkTable")
			print("Could not find _controllerData in NetworkTable")
			return None

		_port = str(self._port)

		if not (_port in NetworkTable.networkTable["_controllerData"]):
			# raise Exception("Could not find device on port " + _port + " in controllerData on NetworkTable")
			print("Could not find device on port " + _port + " in controllerData on NetworkTable")
			return None

		if (NetworkTable.networkTable["_controllerData"][_port] is None):
			# raise Exception("Device data on port " + _port + " is null.")
			print("Device data on port " + _port + " is null.")
			return None

		return NetworkTable.networkTable["_controllerData"][_port]

	# Returns a boolean
	def getButton(self, index):

		_port = self._port
		deviceData = self.getDeviceDataFromTable()

		if (deviceData == None): return None

		if ("buttonStates" in deviceData is None):
			print("2")
			raise Exception("No Button States data found for " + self.getDeviceName() + " on port " + _port)

		if (index >= len(deviceData["buttonStates"])):
			print("3)")
			raise Exception("Button Index " + index + " out of bounds on '" + self.getDeviceName() + "' on port " + _port)
		
		return deviceData["buttonStates"][index]

	# Returns a value between -1 and 1
	def getAxis(self, index):

		if (deviceData == None): return None

		_port = self._port
		deviceData = self.getDeviceDataFromTable()

		if ("axisStates" in deviceData is None):
			raise Exception("No Axis States data found for " + self.getDeviceName() + " on port " + _port)

		if (index >= len(deviceData["axisStates"])):
			raise Exception("Axis Index " + index + " out of bounds on '" + self.getDeviceName() + "' on port " + _port)
		
		if (abs(deviceData["axisStates"][index]) > axisDeadZone):
			return deviceData["axisStates"][index]
		return 0

	# Unknown yet
	def povHat(self, index):
		pass

	# Helper Methods
	def setAxisDeadZone(self, axisDeadZone):
		if (self.axisDeadZone < 0):
			print("Cannot set deadzone to a value less than 0.")
			return 0

		self.axisDeadZone = axisDeadZone

	def getAxisDeadZone(self):
		return self.axisDeadZone

	def getPort(self):
		return self._port

	# Generic Device Information
	def getDeviceName(self):
		deviceData = self.getDeviceDataFromTable()
		if (deviceData == None): return None
		return deviceData["description"]

	def getDeviceVendorID(self):
		deviceData = self.getDeviceDataFromTable()
		if (deviceData == None): return None
		return deviceData["vendorID"]

	def getDeviceProductID(self):
		deviceData = self.getDeviceDataFromTable()
		if (deviceData == None): return None
		return deviceData["productID"]

