import GamepadDevice

class LogitechDualAction(GamepadDevice.DeviceInterface):

	def __init__(self, port):
		super().__init__(port)

	# Button Pad

	def getOneButton(self):
		return super().getButton(0)

	def getTwoButton(self):
		return super().getButton(1)

	def getThreeButton(self):
		return super().getButton(2)

	def getFourButton(self):
		return super().getButton(3)

	# Thumbsticks

	def getLeftThumbstickYAxis(self):
		return super().getAxis(0)

	def getLeftThumbstickXAxis(self):
		return super().getAxis(1)

	def getRightThumbstickYAxis(self):
		return super().getAxis(0)

	def getRightThumbstickXAxis(self):
		return super().getAxis(1)

	def getLeftThumbstickButton(self):
		return super().getButton()

	def getRightThumbstickButton(self):
		return super().getButton()

	# Triggers and Bumpers

	def getLeftTrigger(self):
		return super().getButton()

	def getRightTrigger(self):
		return super().getButton()

	def getLeftBumper(self):
		return super().getButton()

	def getRightBumper(self):
		return super().getButton()

	# D-Pad Hat POV

	def getDPadUpButton(self):
		return super().getButton()

	def getDPadDownButton(self):
		return super().getButton()

	def getDPadLeftButton(self):
		return super().getButton()

	def getDPadRightButton(self):
		return super().getButton()
