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
		self.device = None
		self.fanPower = 'off'
		self.fanSpeed = 0.5
		self.fanPowerPin = 3
		self.fanPostivePin = 5
		self.fanNegativePin = 6

		self.connect()
		self.set_pin_mode_digital(self.fanPowerPin)
		self.set_pin_mode_PWM(self.fanPostivePin)
		self.set_pin_mode_PWM(self.fanNegativePin)
		print("[BLE] initialization done!!")

	def connect(self):
		self.device = pexpect.spawn(CMD_CONNECT,logfile=None, searchwindowsize=200)
		self.device.sendline('connect')
		self.device.expect('Connection successful')
		print("Connection successful")
		print(self.device.before)

	def fanPowerSwitch(self):
		if self.fanPower == 'on':
			self.send_pin_value_digital(self.fanPowerPin, 0)
			self.fanPower = 'off'
		else:
			self.fanPower = 'on'
			self.send_pin_value_digital(self.fanPowerPin, 1)
			time.sleep(0.5)
			self.send_pin_value_PWM(self.fanPostivePin, int(0.8*255))
			time.sleep(0.3)
			self.send_pin_value_PWM(self.fanPostivePin, int(self.fanSpeed*255))
			
	def speedUpFan(self):
		if self.fanPower == 'off':
			return '電風扇未開啟'
		else:
			if self.fanSpeed < 1:
				self.fanSpeed += 0.1
				self.send_pin_value_PWM(self.fanPostivePin, int(self.fanSpeed*255))
			else:
				return '風量已達最大' # fan is full speed
	def speedDownFan(self):
		if self.fanPower == 'off':
			return '電風扇未開啟' # fan is not on
		else:
			if self.fanSpeed > 0.1:
				self.fanSpeed -= 0.1
				send_pin_value_PWM(self.fanPostivePin, self.fanSpeed*255)
			else:
				return '風量已達最低' # fan is lowest speed

	def set_pin_mode_digital(self, pin):
		cmd = 'char-write-cmd 0x000e 0x53{:02x}01'.format(pin)
		self.device.sendline(cmd)

	def set_pin_mode_PWM(self, pin):
		cmd = 'char-write-cmd 0x000e 0x53{:02x}03'.format(pin)
		self.device.sendline(cmd)

	def send_pin_value_PWM(self, pin, value):
		cmd = 'char-write-cmd 0x000e 0x4E{:02x}{:02x}'.format(pin, value)
		# print(cmd)
		self.device.sendline(cmd)

	def send_pin_value_digital(self, pin, value):
		cmd = 'char-write-cmd 0x000e 0x54{:02x}{:02x}'.format(pin, value)
		# print(cmd)
		self.device.sendline(cmd)

if __name__ == '__main__':
	print("START")
	fan = BLEdevice()
	time.sleep(5)
	print("turn fan on")
	fan.fanPowerSwitch()
	time.sleep(5)
	print("speed up")
	fan.speedUpFan()
	time.sleep(5)
	print("turn off")
	fan.fanPowerSwitch()
	time.sleep(5)
	## 下面還沒改
	# BLE = pexpect.spawn(CMD_CONNECT,logfile=None, searchwindowsize=200)
	# BLE.sendline('connect')
	# print("Connect success")
	# BLE.expect(r'Connection successful',timeout=initialization_timeout)
	# # BLE.sendline('char-write-cmd 0x000e 0x530301')
	# set_pin_mode_PWM(3)
	# while True:
	# 	for i in range(0,255):
	# 		send_pin_value_PWM(3,i)
	# 	time.sleep(0.5)
	# 	for i in range(0,255):
	# 		send_pin_value_PWM(3,i)
	# 	time.sleep(0.5)
	# BLE.expect(pexect.EOF)