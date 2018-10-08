# RaspberryRIO
Version: 0.0.1

The RaspberryRIO is a python-based robot controller inspired by the NI roboRIO used by FIRST Robotis Teams.

This is a pet concept project with few features and limited testing.

## Required Items
- [RaspberryPi 3 Model B+](https://www.adafruit.com/product/3775)
- Windows/Mac/Linux PC with wireless capabilities
- [16-Channel PMWM/Servo HAT for Raspberry Pi](https://www.adafruit.com/product/2327)

This assumes your RaspberryPi 3B+ is capable of running Python, I recommend the linux distro Raspbian (2018-latest) as that is the version I have. Your RaspberryPi must also have I2C enabled, and the required python packages for the PCA9685 PWM HAT installed. This also assumes you have adequate power supply, and have wired up the PWM Hat to the Pi adequately.

If this project proves successul, I will add the image of my RaspberryPi's SD card for easier cloning and setup. I will also provide a tutorial on how to wire up your Pi.

## How It Works
The robot is controlled through a master Python script that loads a custom user-made Robot.py script. The Raspberry Pi broadcasts its own SSD for the ControlStation to connect to.
The ControlStation handles the gamepad controller inputs and sends and receives data to the Pi bot. The ControlStation is built using NodeJS and Electron.
