import time
import datetime
import sys
import clr
clr.AddReferenceToFileAndPath(r"Core.dll")
import R2Core
clr.ImportExtensions(R2Core)

class WeatherEntry(object):

    def __init__(self, entry):
        self.timestamp = entry.validTime
        self.temperature = self.get_parameter(entry, "t")
        self.cloud_cover = (self.get_parameter(entry, "tcc_mean") / 8.0) * 100
        self.humidity = self.get_parameter(entry, "r")
        self.precipitation = float(self.get_parameter(entry, "pmean"))

    def get_parameter(self, entry, name):
        for parameter in entry.parameters:
            if parameter.name == name:
                return parameter.values[0] or 0.0
        return None

class MainClass:

    def r2_init(self):
        self.settings = self.device_manager.Get("settings")
        self.l = self.device_manager.Get(self.settings.I.Logger())
        self.web_factory = self.device_manager.Get(self.settings.I.WebFactory())
        self.client = self.web_factory.CreateHttpClient("http_client")
        self.lat = None
        self.lon = None
        self.entries = []

    def setup(self):
        if self.lat == None or self.lon == None:
            self.l.error("smhi.py: self.lat & self.lon needs to be set to string values")
        self.message = self.web_factory.CreateHttpMessage("https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/" + self.lon +"/lat/" + self.lat + "/data.json")
        self.message.Method = "GET"

    @property
    def max_temperature(self):
        if not self.entries:
            self.l.warn("smhi.py: No entries loaded. use load_today in order to make sure you have updated values.")
            return 0
        
        max_temperature = -273.15
        for entry in self.entries:
            if (entry.temperature > max_temperature):
                max_temperature = entry.temperature

        return max_temperature

    @property
    def total_percipitation(self):
        
        if not self.entries:
            self.l.warn("smhi.py: No entries loaded. use load_today in order to make sure you have updated values.")
            return 0
        
        percipitation = float(0.0)
        for entry in self.entries:
            percipitation = percipitation + entry.precipitation
        
        return percipitation

    def load(self):
        self.setup()
        self.response = self.client.Send(self.message)
        if self.response.Code != 200:
            self.l.error("SMHI: Response returned code: " + str(self.response.Code))
        else:
            for entry in self.response.Payload.timeSeries:
                yield entry

    def load_tomorrow(self):
        for entry in self.load():
            if (entry.validTime.IsTomorrow()):
                entryModel = WeatherEntry(entry)
                self.entries.append(entryModel)
        self.l.info("smhi: did load tomorrow", "water")

    def load_today(self):
        for entry in self.load():
            if (entry.validTime.IsToday()):
                entryModel = WeatherEntry(entry)
                self.entries.append(entryModel)
        self.l.info("smhi: did load today", "water")
	
    def print_entries(self):
        for entry in self.entries:
            self.l.message("T: " + str(entry.temperature) + " H: " + str(entry.humidity) + " C: " + str(entry.cloud_cover) + " P: " + str(entry.precipitation) + " T: " + str(entry.timestamp))
    
    def debug_configure_nacka(self):
        self.lat = "59.3226"
        self.lon = "18.2097"

    def loop(self):
        time.sleep(60)
        return False

main_class = MainClass()
