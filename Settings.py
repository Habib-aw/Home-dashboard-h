from datetime import datetime
from enum import Enum

# class syntax
class PrayerName(Enum):
    FAJR = 1
    ZUHR = 2
    ASR = 3
    MAGHRIB = 4
    ISHA = 5

# functional syntax
PrayerName = Enum('PrayerName', ['FAJR', 'ZUHR', 'ASR','MAGHRIB','ISHA'])
maxColumnSpan=7
prayerFrameSpan = 4

prayerFrameBgColor= "black"
notesFrameBgColor= "black"
weatherFrameBgColor= "black"
dateTimeFrameBgColor= "black"

firstJammahSummer = "1:30"
secondJammahSummer = "1:50"

firstJammahWinter = "1:00"
secondJammahWinter = "1:20"

today = datetime.today()
month= today.month-1
day = today.day-1
year = today.year
minsBeforeSalah = 15
prayerFontSize = 70
notPrayerFontSize = 30
mithlFontSize = 25

hourlyWeatherIconWidth= 100
hourlyWeatherIconHeight= 100
dailyWeatherIconHeight= 100
dailyWeatherIconWidth= 100
hourlyWeatherDataFontSize = 30
hourlyWeatherHeadingFontSize = 20
dailyDayFontSize = 30
dailyTempFontSize = 40

notesTitleFontSize = 53
notesTextFontSize = 30
dateFontSize = 100
clockFontSize = 100
numOfWeatherHours = 8

hourlyWeatherPaddingX=10
forecastsPaddingX=30
prayerLabelsPaddingX = 36
otherPrayerLabelsPaddingX = 0


hourWeatherCheckInterval = 10 #min
adhaanCheckInterval = 1 # sec
prayerPassedCheckInterval =1 # min

prayerFramePadY = 15
notesFramePadY = 0
weatherFramePadY = 0
dateTimeFramePadY = 0