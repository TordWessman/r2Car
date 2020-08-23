import scriptbase
import time
import random
import clr
clr.AddReferenceToFileAndPath(r"PushNotifications.dll")
import R2Core.PushNotifications
clr.ImportExtensions(R2Core.PushNotifications)

class MainClass:

    def r2_init(self):
        self.l = self.device_manager.Get("log")
        self.settings = self.device_manager.Get("settings")

    def message(self, message):
        push_factory = self.device_manager.Get(self.settings.I.PushFactory())
        proxy = self.device_manager.Get(self.settings.I.PushProxy())
        message = push_factory.CreatePush(message, "sthlm_moist", "test_group")
        proxy.Broadcast(message)

    def loop(self):		
        time.sleep(0.5)
        return False


main_class = MainClass()

