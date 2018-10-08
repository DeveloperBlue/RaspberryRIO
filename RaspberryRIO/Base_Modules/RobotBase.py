# import Adafruit_PCA9685
import time

global __PWMInterface
# __PWMInterface = Adafruit_PCA9685.Adafruit_PCA9685()

class RobotBase:

	# Properties
	__enabled = False

	def __init__(self):
		pass

	# User Set up
	def robotInit(self):
		print("WARN: No custom robotInit Method was defined.")

	def operatorControl(self):
		print("WARN: No Operator Control Method was defined.")

	def disable(self):
		print("WARN: No custom Disable Method was defined.")

	# Important
	def _enable(self):
		print("<ENABLING ROBOT>")
		self.__enabled = True

	def _disable(self):
		print("<DISABLING ROBOT>")
		self.__enabled = False
		self._stopAllPWMs()

	def _stopAllPWMs(self):
		print("Sending signal to stop all PWM Devices . . .")
		try:
			__PWMInterface.set_all_pwm(0, 0)
		except Exception as error:
			print("SERIOUS: Failed to stop all PWM Devices.")
			raise Exception(error)


	# Helper Methods

	def isEnabled(self):
		return self.__enabled

	def isDisabled(self):
		return not self.__enabled

	def _getStates(self):
		return {
			"enabled":self.__enabled
		}


# PWM Objects

class PWMBasedObject:

	lastPulseRatio = 0

	def __init__(sef, pwmIndex, minPulse, maxPulse, frequency):

		self.pwmIndex = pwmIndex
		self.minPulse = minPulse
		self.maxPulse = maxPulse
		self.frequency = frequency

	def setPulse(self, pulse):
		pulse_length = 1000000    # 1,000,000 us per second
		pulse_length //= 60       # 60 Hz
		print('{0}us per period'.format(pulse_length))
		pulse_length //= 4096     # 12 bits of resolution
		print('{0}us per bit'.format(pulse_length))
		pulse *= 1000
		pulse //= pulse_length
		__PWMInterface.set_pwm(pwmIndex, 0, pulse)

	def setPulseRatio(self, pulseRatio):

		if (pulseRatio > 1):
			pulseRatio = 1
		if (pulseRatio < -1):
			pulseRatio = -1

		self.lastPulseRatio = pulseRatio

		self.minPulse + ((self.maxPulse - self.minPulse)*pulseRatio)

	def getLastPulseRatio(self):
		return self.lastPulseRatio


	## Helpers

	def setMinPulse(self, minPulse):
		self.minPulse = minPulse

	def setMaxPulse(self, maxPulse):
		self.maxPulse = maxPulse

	def setFrequency(self, frequency):
		self.frequency = frequency

	def getPWMIndex(self):
		return self.pwmIndex

	def getMinPulse(self):
		return self.minPulse

	def getMaxPulse(self):
		return self.maxPulse

	def getFrequency(self):
		return self.frequency


class Servo(PWMBasedObject):

	def __init__(self, pwmIndex):
		PWMBasedObject.__init__(self, pwmIndex, 150, 600, 60)

	def setAngle(self, angle):
		setPulse(self.minPulse + ((self.maxPulse - self.minPulse)*(angle/180)))

		# x = (a + ((b - a)*(o/180)))
		# x - a = (b - a)*(o/180)
		# (x - a)/(b - a) = o/180
		# 180((x-a)/(b-a)) = o


	def getAngle(self):
		return 180((self.getPulse() - self.minPulse)/(self.maxPulse - self.minPulse))


class Spark(PWMBasedObject):

	inverted = False

	def __init__(self, pwmIndex):
		PWMBaseObject.__init__(self, pwmIndex, 1000, 2000, 50)

	def setSpeed(self, speed):

		if (self.inverted):
			self.speed = self.speed * -1

		self.setPulseRatio(speed)

	def getSpeed(self):
		self.getLastPulseRatio()

	def setInverted(self, inverted):
		self.inverted = inverted

	def getInverted(self):
		return self.inverted
