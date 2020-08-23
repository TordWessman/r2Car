import scriptbase
import time
import clr
clr.AddReferenceToFileAndPath(r"Core.dll")
from R2Core import *
clr.AddReferenceToFileAndPath(r"PushNotifications.dll")
import R2Core.PushNotifications
clr.ImportExtensions(R2Core.PushNotifications)
clr.AddReferenceToFileAndPath(r"MainFrame.exe")
import MainFrame
clr.ImportExtensions(MainFrame)
#import obd

class MainClass:

	def r2_init(self):
		self.settings = self.device_manager.Get("settings")
		self.l = self.device_manager.Get(self.settings.I.Logger())
		self.l.LogLevel = LogLevel.Info
		self.device_manager.Get(self.settings.I.FileLogger()).LogLevel = LogLevel.Info
		self.script_factory = self.device_manager.Get(self.settings.I.PythonScriptFactory())
		self.web_factory = self.device_manager.Get(self.settings.I.WebFactory())
		common_factory = self.device_manager.Get(self.settings.I.DeviceFactory())
		self.identity = common_factory.CreateIdentity("router")
		self.device_manager.Add(self.identity)
		self.setup_vars()
		self.set_up_servers()
		self.set_up_push()
		self.should_run = False

	def setup_vars(self):
		self.tcp_port = self.settings.C.DefaultTcpPort()
		self.http_port = self.settings.C.DefaultHttpPort()
		self.udp_port = self.settings.C.DefaultBroadcastPort()
		self.camera_port = "4444"

	def set_up_servers(self):
		self.http_server = self.web_factory.CreateHttpServer(self.settings.I.HttpServer(), self.http_port)
		self.tcp_server = self.web_factory.CreateTcpServer(self.settings.I.TcpServer(), self.tcp_port)
		self.device_manager.Add(self.http_server)
		self.device_manager.Add(self.tcp_server)
		self.http_server.Start()
		self.tcp_server.Start()

		#tcp_router_endpoint = self.web_factory.CreateTcpRouterEndpoint(self.tcp_server)
		#self.http_server.AddEndpoint(tcp_router_endpoint)
		#self.tcp_server.AddEndpoint(tcp_router_endpoint)
		self.router_address = "axelit.se"
		self.l.message("Attaching to router: " + self.router_address)
		self.client_server = self.web_factory.CreateTcpClientServer("client_server")
		self.client_server.Configure(self.identity, self.router_address, self.settings.C.DefaultTcpPort())
		self.client_server.Start()
		self.client_server.AddServer(self.settings.C.ConnectionRouterHeaderServerTypeHTTP(), self.http_server)
		self.client_server.AddServer(self.settings.C.ConnectionRouterHeaderServerTypeTCP(), self.tcp_server)
		self.device_manager.Add(self.client_server)


	def set_up_push(self):
		push_factory = self.device_manager.Get(self.settings.I.PushFactory())
		storage = push_factory.CreateStorage(self.settings.I.PushStorage())
		proxy = push_factory.CreateProxy(self.settings.I.PushProxy(), storage)
		apple = push_factory.CreateAppleFacade(self.settings.I.PushAppleFacade(), self.settings.C.AppleCertPassword(), self.settings.C.AppleCert())
		proxy.AddFacade(apple)
		self.device_manager.Add(storage)
		self.device_manager.Add(proxy)

	def setup(self):
		self.l.message("setup")

	def stop(self):
		self.should_run = False

	def loop(self):
		return False


main_class = MainClass()
