from hijri_converter import Gregorian
from datetime import datetime,timedelta
import json
class Ramadan:
    def __init__(self) -> None:
        today = datetime.today()
        tmrro = today + timedelta(days=1)

        day = today.day
        month = today.month
        self.hijri = Gregorian(int(datetime.now().year), month, day).to_hijri()

        self.data = json.load(open("2025.json"))

        self.todaySehri = self.data[month-1][day-1]['Fajr_start']
        self.todayIftaar = self.data[month-1][day-1]['Maghrib_start']

        self.tmrroSehri = self.data[tmrro.month-1][tmrro.day-1]['Fajr_start']
        self.tmrroIftaar = self.data[tmrro.month-1][tmrro.day-1]['Maghrib_start']

    def isRamadan(self):
        if self.hijri.month_name() =="Ramadhan":
            return True
        return False

    def getRamadanDay(self):
        return self.hijri.day
