from Settings import prayerFrameBgColor
from tkinter import Label
import json
from Settings import today, month, day, year, minsBeforeSalah, notPrayerFontSize,prayerFontSize, prayerLabelsPaddingX, otherPrayerLabelsPaddingX, adhaanCheckInterval, prayerPassedCheckInterval
from Jummah import firstJammah, secondJammah
from datetime import datetime, timedelta
from audioplayer import AudioPlayer
from threading import Thread
import schedule
import requests

def playNoise(soundFile):
    AudioPlayer("Sounds/" + soundFile + ".mp3").play(block=True)

class Prayers:
    def __init__(self,frame,sehriText,sehriLabel,iftaarText,iftaarLabel):
        self.sehriText = sehriText
        self.sehriLabel = sehriLabel
        self.iftaarText = iftaarText
        self.iftaarLabel = iftaarLabel
        self.frame = frame
        self.prayerLength = 5
        self.schedulerSet = False
        self.getPrayersScheduler = None
        self.prayerTimeObj = [None for _ in range(6)]
        self.prayerLabels = [[None for _ in range(6)] for _ in range(2)]
        self.getPrayers()
        self.adhaanAnnounce = False
        self.startAnnounceIndex = 0
        self.salahAnnounceIndex = 0
        self.salahAnnounce = False
        schedule.every(adhaanCheckInterval).seconds.do(self.announceAdhaanAndSalah)

    def salahsToDate(self):
        index = 0
        if self.prayers[1][1] != "":
            for i in range(1, 2):
                for j in range(1, 7):
                    # print(self.prayers[i][j],i,j)
                    salahsSplit = self.prayers[i][j].split(":")
                    if j == 1 or (j == 2 and (salahsSplit[0] == "12" or salahsSplit[0] == "11")):
                        self.prayerTimeObj[index] = datetime(year, month + 1, day + 1, int(salahsSplit[0]), int(salahsSplit[1]))
                    else:
                        self.prayerTimeObj[index] = datetime(year, month + 1, day + 1, int(salahsSplit[0]) + 12, int(salahsSplit[1]))
                    index+=1
        
        self.prayers[1][6] = getTahajjudTime(self.prayerTimeObj[0])
        self.prayerTimeObj[0] = getTahajjudDateTime(self.prayerTimeObj[0])
        self.prayers[2][5] = getMiddleOfNight(self.prayerTimeObj[3])
        self.tmrro_tahajjud = getTmrroTahajjudTime(self.prayerTimeObj[3])
    def getPrayers(self):
        try:
            # res = requests.get('https://data.baitulmamur.academy/')
            # self.data = json.loads(res.text)
            self.data = json.load(open(str(today.year)+".json"))
            self.prayers = [
                ["", "Fajr", "Zuhr", "Asr", "Maghrib", "Isha","Tahajjud Last Third"],
                ["Start",self.data[month][day]['Fajr_start'], self.data[month][day]['Zuhr_start'], self.data[month][day]['Asr_start2'], self.data[month][day]['Maghrib_start'], self.data[month][day]['Isha_start'], self.data[month][day]['Isha_start']],
                ["End",  self.data[month][day]['Sunrise'],"-", "-", "-", "", "-"]
            ]
            # try:
            self.salahsToDate()
            # except Exception as e:
            #     print("*************************",e,"*****************")
            schedule.cancel_job(self.getPrayersScheduler)
            self.schedulerSet = False
        except Exception as e:
            print("Error!\n\n", e)
            self.prayers = [
                ["","Fajr", "Zuhr", "Asr", "Maghrib", "Isha","Tahajjud Last Third"],
                ["Start", "","", "", "", "", ""],
                ["End", "","", "", "", "", ""]

            ]

            if not self.schedulerSet:
                self.schedulerSet = True
                self.getPrayersScheduler = schedule.every(2).minutes.do(self.getPrayers)
        self.showPrayers()

    def showPrayers(self):
        height = len(self.prayers)
        width = len(self.prayers[0])

        for i in range(height):
            for j in range(width):
                if (i > 0 and i < self.prayerLength) and j != 0:
                    self.prayerLabels[i - 1][j - 1] = Label(self.frame, text=self.prayers[i][j], background=prayerFrameBgColor,font=("Arial", prayerFontSize), foreground="white")
                    self.prayerLabels[i - 1][j - 1].grid(row=i, column=j, ipadx=prayerLabelsPaddingX)
                else:
                    font =notPrayerFontSize
                    if i==0 and j == 6: # here
                        font = notPrayerFontSize - 7
                    notPrayer = Label(self.frame, text=self.prayers[i][j], background=prayerFrameBgColor,
                                      font=("Arial", font), foreground="white")
                    notPrayer.grid(row=i, column=j, ipadx=otherPrayerLabelsPaddingX)
        if self.prayers[1][1] != "":
            self.checkPrayerPassed()

    def checkPrayerPassed(self):
        if self.prayers[1][1] != "":
            for i in range(len(self.prayerTimeObj)):
                if (self.prayerTimeObj[i] < datetime.now()):
                    if i == 5:
                        continue
                    self.prayerLabels[0][i].config(background="green")
                    if i == 0:
                        self.sehriLabel.config(text=self.sehriText)
                        self.prayerLabels[0][5].config(text=self.tmrro_tahajjud)
                    if i == 3:
                        self.iftaarLabel.config(text=self.iftaarText)
            for i in range(len(self.prayerTimeObj)):
                if i == 0:
                    if datetime.now() > getSunriseDateTime():
                        self.prayerLabels[0][i].config(background="red")
                if i == len(self.prayerTimeObj) - 2:
                    if(datetime.now()>  getMiddleOfNightDateTime(self.prayerTimeObj[4])):
                        self.prayerLabels[0][i].config(background="red")
                    break
                if (self.prayerTimeObj[i + 1] < datetime.now()):
                    self.prayerLabels[0][i].config(background="red")


    def announceAdhaanAndSalah(self):
        if self.prayers[1][1] != "":
            for i in range(len(self.prayerTimeObj)):
                if (datetime.now() >= self.prayerTimeObj[i] and datetime.now() < (self.prayerTimeObj[i] + timedelta(minutes=1))) and not self.adhaanAnnounce:
                    self.adhaanAnnounce = True
                    self.startAnnounceIndex = i
                    self.checkPrayerPassed()
                    if i == 5:
                        Thread(target=playNoise, args=("salah",)).start()
                    elif i == 0:
                        Thread(target=playNoise, args=("adhaan-new",)).start()
                    else:
                        Thread(target=playNoise, args=("full-adhaan",)).start()
                    break
            if not (datetime.now() >= self.prayerTimeObj[self.startAnnounceIndex] and datetime.now() < (
                    self.prayerTimeObj[self.startAnnounceIndex] + timedelta(minutes=1))):
                self.adhaanAnnounce = False
def getYesterdayMaghrib():
    yesterday = datetime.now() - timedelta(days=1)
    yesterdayMaghrib =  json.load(open(str(today.year)+".json"))[yesterday.month-1][yesterday.day-1]['Maghrib_start']
    salahsSplit = yesterdayMaghrib.split(":")
    yesterdayMaghribObject =  datetime(yesterday.year, yesterday.month, yesterday.day, int(salahsSplit[0]) + 12, int(salahsSplit[1]))
    return yesterdayMaghribObject
def getNightLength(Fajr):
    return Fajr - getYesterdayMaghrib()
def getTmrroNightLength(Maghrib):
    return getTmrroFajr()-Maghrib
def getTahajjudDateTime(Fajr):
    thirdNightLength = getNightLength(Fajr)/3
    tahajjudDateTime= Fajr - thirdNightLength
    return tahajjudDateTime
def getTahajjudTime(Fajr):
    tahajjudDateTime = getTahajjudDateTime(Fajr)
    t_min = str(tahajjudDateTime.minute)
    t_hour = str(tahajjudDateTime.hour)
    if len(t_min) == 1:
        return t_hour+":0" + t_min
    return t_hour+":" + t_min
def getMiddleOfNightDateTime(Maghrib):
    halfNightLength = getTmrroNightLength(Maghrib)/2
    middleOfNight= Maghrib + halfNightLength
    return middleOfNight
def getTmrroTahajjudTime(Maghrib):
    third_night_length = getTmrroNightLength(Maghrib)/3
    tmrroTahajjudTime = Maghrib + (third_night_length*2)
    
    return tmrroTahajjudTime.strftime("%-I:%M")
def getTmrroFajr():
    tmrro = datetime.now() + timedelta(days=1)
    tmrroFajr =  json.load(open(str(today.year)+".json"))[tmrro.month-1][tmrro.day-1]['Fajr_start']
    salahsSplit = tmrroFajr.split(":")
    tmrroFajrObject =  datetime(tmrro.year, tmrro.month, tmrro.day, int(salahsSplit[0]) , int(salahsSplit[1]))
    return tmrroFajrObject
def getMiddleOfNight(Maghrib):
    middleOfNight  = getMiddleOfNightDateTime(Maghrib)
    hour = middleOfNight.hour
    if hour > 12:
        hour -=12
    return str(hour) +":" +str(middleOfNight.minute)
def getSunriseDateTime():
    sunriseTime = json.load(open(str(today.year)+".json"))[today.month-1][today.day-1]['Sunrise']
    salahsSplit = sunriseTime.split(":")
    sunriseTimeObject =  datetime(today.year, today.month, today.day, int(salahsSplit[0]) , int(salahsSplit[1]))
    return sunriseTimeObject