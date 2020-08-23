import scriptbase
import time

class MainClass:

	password = "mamma"
	login = "olga"
	URL = "http://hej.axelit.se/logins"
	log = ""

	def r2_init(self):
		self.log = self.device_manager.Get("log")
		self.server = self.device_manager.Get("tcp_server")
		self.memory = self.device_manager.Get("memory")
		self.device_factory = self.device_manager.Get("device_factory")
		self.web_factory = self.device_manager.Get("web_factory")
		self.http_client = self.web_factory.CreateHttpClient("http_clientX")
		self.jmf = self.device_factory.CreateJsonMessageFactory("jmf")

	def setup(self):
		self.log.message("shetup")

	def loop(self):
		self.log.message("SENDING TO: " + self.URL)
		token = self.memory.Get("client_token")
		port = str(self.server.Port)
		payload = self.jmf.CreateRegister(self.login,self.password,token.Value,port)
		message = self.web_factory.CreateHttpMessage(self.URL)
		message.Payload = payload
		self.http_client.Send(message)
		time.sleep(30)
		return True


main_class = MainClass()

