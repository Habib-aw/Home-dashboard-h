### AUTO UPDATE JUMMAH TIMES
from datetime import timedelta,datetime
from Settings import firstJammahSummer,firstJammahWinter,secondJammahSummer,secondJammahWinter


minutesAfterJummahChange = 10



def lastDayOfMonth(dayOfWeek,dateTimeObj):
    daysOfWeek = ['sunday','monday','tuesday','wednesday',
                        'thursday','friday','saturday']
    chosenDay = daysOfWeek.index(dayOfWeek.lower())
    isoDay = chosenDay - dateTimeObj.isoweekday()
    if isoDay >= 0: isoDay -= 7 # go back 7 days
    return dateTimeObj + timedelta(days=isoDay)
def strArrayToInt(arr):
    for i in range(len(arr)):
        arr[i] = int(arr[i])
    sJPlusMinAfterJummah= arr[1]+minutesAfterJummahChange
    arr[0]=arr[0] + (sJPlusMinAfterJummah//60)
    arr[1]= sJPlusMinAfterJummah%60
    return arr

firstJammah = firstJammahWinter
secondJammah = secondJammahWinter


sJS = strArrayToInt(secondJammahSummer.split(":"))
sJW = strArrayToInt(secondJammahWinter.split(":"))
marchLastSunday = lastDayOfMonth('sunday',datetime(datetime.now().year,4,1,sJW[0],sJW[1]))
lastWinterJummah= marchLastSunday-timedelta(2)
octoberLastSunday = lastDayOfMonth('sunday',datetime(datetime.now().year,11,1,sJS[0],sJS[1]))
lastSummerJummah = octoberLastSunday-timedelta(2)
if datetime.now() >= lastWinterJummah and datetime.now() <=lastSummerJummah:
    firstJammah = firstJammahSummer
    secondJammah=secondJammahSummer
