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

	def connect(self):
		device = pexpect.spawn(CMD_CONNECT,logfile=None, searchwindowsize=200)


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