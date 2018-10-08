import RobotBase
import time
import LogitechDualAction

class Robot(RobotBase.RobotBase):

	controller = None

	# Construtor
	def __init__(self):
		super().__init__()

	# User-Defined Methods
	def robotInit(self):
		self.controller = LogitechDualAction.LogitechDualAction(0)
		print("Controller Status 0", self.controller)

	def operatorControl(self):

		print("Operator Control Enabled")

		while super().isEnabled():

			if self.controller.getOneButton():
				print("Houston we have liftoff!")

			time.sleep(0.02)

		print("Operator Control Ended")