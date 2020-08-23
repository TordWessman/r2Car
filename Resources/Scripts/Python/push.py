import time
import random
import clr
clr.AddReferenceToFileAndPath(r"PushNotifications.dll")
import R2Core.PushNotifications
clr.ImportExtensions(R2Core.PushNotifications)

class MainClass:

    def r2_init(self):
        self.settings = self.device_manager.Get("settings")
        self.push_factory = self.device_manager.Get(self.settings.I.PushFactory())
        self.proxy = self.device_manager.Get(self.settings.I.PushProxy())
        self.identity = "sthlm_moist"

    def send(self, message, group):
        message = self.push_factory.CreateSimple(message, self.identity, group)
        self.proxy.Broadcast(message)

    def loop(self):		
        time.sleep(0.5)
        return False


main_class = MainClass()

