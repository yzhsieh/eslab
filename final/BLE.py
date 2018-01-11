import pexpect
import time
import sys
###
initialization_timeout = 3
###
CMD_CONNECT = 'sudo gatttool -b D5:3A:73:E3:F0:7E -t random --interactive'
BLE = None
###
class BLEdevice:
	def __init__(self):
		device = None
		fanCurrentPower = 'off'
		fanCurrentSpeed = 0.5
		fanPowerPin = 3
		fanPostivePin = 5
		fanNegativePin = 6

		connect()
		set_pin_mode_digital(fanPowerPin)
		set_pin_mode_PWM(fanPostivePin)
		set_pin_mode_PWM(fanNegativePin)

	def connect(self):
		device = pexpect.spawn(CMD_CONNECT,logfile=None, searchwindowsize=200)

	def fanPowerSwitch(self):
		if fanCurrentPower == 'on':
			send_pin_value_digital(fanPowerPin, 0)
			fanCurrentPower = 'off'
		else:
			send_pin_value_digital(fanPowerPin, 1)
			time.sleep(0.5)
			send_pin_value_PWM(fanPostivePin, 0.8*255)
			time.sleep(0.3)
			send_pin_value_PWM(fanPostivePin, fanCurrentSpeed*255)
			
	def speedUpFan(self):
		if fanCurrentPower == 'off':
			return 'err0' # fan is not on
		else:
			if fanCurrentSpeed < 1:
				fanCurrentSpeed += 0.1
				send_pin_value_PWM(fanPostivePin, fanCurrentSpeed*255)
			else:
				return 'err1' # fan is full speed
	def speedDownFan(self):
		if fanCurrentPower == 'off':
			return 'err0' # fan is not on
		else:
			if fanCurrentSpeed > 0.1:
				fanCurrentSpeed -= 0.1
				send_pin_value_PWM(fanPostivePin, fanCurrentSpeed*255)
			else:
				return 'err1' # fan is lowest speed

	def set_pin_mode_digital(self, pin):
		cmd = 'char-write-cmd 0x000e 0x53{:02x}01'.format(pin)
		BLE.sendline(cmd)

	def set_pin_mode_PWM(self, pin):
		cmd = 'char-write-cmd 0x000e 0x53{:02x}03'.format(pin)
		BLE.sendline(cmd)

	def send_pin_value_PWM(self, pin, value):
		cmd = 'char-write-cmd 0x000e 0x4E{:02x}{:02x}'.format(pin, value)
		# print(cmd)
		BLE.sendline(cmd)

	def send_pin_value_digital(self, pin, value):
		cmd = 'char-write-cmd 0x000e 0x54{:02x}{:02x}'.format(pin, value)
		print(cmd)
		BLE.sendline(cmd)

if __name__ == '__main__':
	print("START")

	## 下面還沒改
	BLE = pexpect.spawn(CMD_CONNECT,logfile=None, searchwindowsize=200)
	BLE.sendline('connect')
	print("Connect success")
	BLE.expect(r'Connection successful',timeout=initialization_timeout)
	# BLE.sendline('char-write-cmd 0x000e 0x530301')
	set_pin_mode_PWM(3)
	while True:
		for i in range(0,255):
			send_pin_value_PWM(3,i)
		time.sleep(0.5)
		for i in range(0,255):
			send_pin_value_PWM(3,i)
		time.sleep(0.5)
	BLE.expect(pexect.EOF)