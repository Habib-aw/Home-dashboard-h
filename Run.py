from tkinter import Tk,Label,Frame
from datetime import datetime
from Weather import Weather
from Settings import prayerFrameBgColor,notesFrameBgColor,weatherFrameBgColor,dateTimeFrameBgColor,today,prayerFrameSpan,maxColumnSpan,clockFontSize,dateFontSize,notesTextFontSize,notesTitleFontSize,prayerFramePadY,notesFramePadY,weatherFramePadY,dateTimeFramePadY
from Prayers import Prayers
from Ramadan import Ramadan
import os
import schedule
root= Tk()


prayerFrame = Frame(root,background=prayerFrameBgColor)
notesFrame = Frame(root,background=notesFrameBgColor)
weatherFrame = Frame(root,background=weatherFrameBgColor)
dateTimeFrame = Frame(root,background=dateTimeFrameBgColor)



notesFrame.pack(fill='x')
weatherFrame.pack()
dateTimeFrame.pack(expand=1)
prayerFrame.pack()
# notesFrame.pack(ipady=notesFramePadY)
# weatherFrame.pack(ipady=dateTimeFramePadY)
# dateTimeFrame.pack(ipady=weatherFramePadY)
# prayerFrame.pack(ipady=prayerFramePadY)



# errorMsgLabel = Label(notesFrame,text="Error, no internet connection",font=("Arial",notesTextFontSize+10),background=notesFrameBgColor,foreground="red")

r = Ramadan()
dayFrame = Frame(notesFrame,background=notesFrameBgColor)
sehriFrame = Frame(notesFrame,background=notesFrameBgColor)
iftaarFrame=Frame(notesFrame,background=notesFrameBgColor)
dayLabel = Label(dayFrame,text="Ramadan Day",font=("Arial",35),background=notesFrameBgColor,foreground="white")
day = Label(dayFrame,text=r.getRamadanDay(),font=("Arial",80),background=notesFrameBgColor,foreground="white")

sehriLabel = Label(sehriFrame,text="Sehri Ends",font=("Arial",35),background=notesFrameBgColor,foreground="white")
sehri = Label(sehriFrame,text=r.todaySehri,font=("Arial",80),background=notesFrameBgColor,foreground="white")

iftaarLabel = Label(iftaarFrame,text="Iftaar Starts",font=("Arial",35),background=notesFrameBgColor,foreground="white")
iftaar = Label(iftaarFrame,text=r.todayIftaar,font=("Arial",80),background=notesFrameBgColor,foreground="white")


dayLabel.pack()
day.pack()
sehriLabel.pack()
sehri.pack()
iftaarLabel.pack()
iftaar.pack()

dayFrame.pack(side="left",expand=True)
sehriFrame.pack(side="left",expand=True)
iftaarFrame.pack(side="right",expand=True)

p = Prayers(prayerFrame,r.tmrroSehri,sehri,r.tmrroIftaar,iftaar)
# p = Prayers(prayerFrame)
# Label(notesFrame,text="Notes",font=("Arial",notesTitleFontSize),background=dateTimeFrameBgColor,foreground="white").pack(side='top')
# w = Weather(weatherFrame,errorMsgLabel)
# if today.strftime("%A") =="Friday":
#     Label(notesFrame,text="- Bid for house",font=("Arial",notesTextFontSize),background=notesFrameBgColor,foreground="white").pack()
clock = Label(dateTimeFrame,text=today.strftime('%I:%M:%S %p'),font=("Arial",clockFontSize),background=dateTimeFrameBgColor,foreground="white")
clock.pack(side="bottom")
Label(dateTimeFrame,text=today.strftime('%A, %d %B %Y'),font=("Arial",dateFontSize),background=dateTimeFrameBgColor,foreground="white").pack(side="bottom")


def repeater():
    time = datetime.now().strftime('%I:%M:%S %p')
    clock.config(text=time)
    if time == "12:00:00 AM":
        os.system("sudo reboot")
    schedule.run_pending()
    clock.after(200,repeater)

repeater()



root.config(bg=dateTimeFrameBgColor)
root.attributes('-fullscreen',True)
root.mainloop() 

# GRID FORMAT IF NECESSARY
# prayerFrame.grid(row=0, column=0, sticky="nsew",columnspan=prayerFrameSpan)
# notesFrame.grid(row=0, column=prayerFrameSpan, sticky="nsew",columnspan=(maxColumnSpan-prayerFrameSpan))
# weatherFrame.grid(row=1, sticky="nsew",columnspan=maxColumnSpan)
# dateTimeFrame.grid(row=2,  sticky="nsew",columnspan=maxColumnSpan)
# for i in range(maxColumnSpan):
#     root.grid_columnconfigure(i, weight=1, uniform="group1")
# root.grid_rowconfigure(0, weight=1)