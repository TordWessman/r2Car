import scriptbase
import time
import clr
clr.AddReferenceToFileAndPath(r"Input.dll")
import R2Core.GPIO
from R2Core.GPIO import SerialConnectionException
from System.IO import IOException

class MainClass:

	def list(self):
		return {"katt","hund"}
		
	def r2_init(self):
		self.l = self.device_manager.Get("log")
		self.led = self.device_manager.Get("lamp")
		self.error_count = 0

	def stop(self):
		self.led.Value = False

	def loop(self):
		self.led.Value = True
		time.sleep(2.0)
		self.led.Value = False
		time.sleep(2.0)
		self.error_count = 0

		return True


main_class = MainClass()
