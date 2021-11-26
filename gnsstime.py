#import erfa
import numpy as np

def getMJD(t):
    return getJulianDay(t)- 2400000.5

def getJulianDay(t):
    #aux=erfa.cal2jd(getYear(t),getMonth(t),getDay(t))
    year=getYear(t)
    month=getMonth(t)
    day=getDay(t)
    h=getSecsOfDay(t)/3600.
    if (month<=2):
        year=year-1
        month=month+12
    JD=np.floor(365.25*year)+np.floor(30.6001*(month+1))+day+1720981.5 +h/24
    return JD#aux[0]+aux[1]

def getGpsWeek(t):
    gps_t0=np.datetime64('1980-01-06T00:00:00')
    return ((t - gps_t0)/ np.timedelta64(1, 'D')/7).astype(np.int64)

def getDayOfYear(t):
    year=t.astype('datetime64[Y]')
    return ((t-year)/np.timedelta64(1,'D')+1).astype(np.int64)

def getSecsOfDay(t):
    today=t.astype('datetime64[D]')
    return (t-today)/ np.timedelta64(1, 's')

def getDayOfWeek(t):
    gps_t0=np.datetime64('1980-01-06T00:00:00')
    return ((t - gps_t0)/ np.timedelta64(1, 'D') % 7).astype(np.int64)

def getSecsOfWeek(t):
    day=t.astype('datetime64[D]')
    secsOfDay=(t-day)/ np.timedelta64(1, 's')
    gps_t0=np.datetime64('1980-01-06T00:00:00')
    dayOfWeek=((t - gps_t0)/ np.timedelta64(1, 'D') % 7).astype(np.int64)
    return secsOfDay+dayOfWeek*24*60*60

def getYear(t):
    return t.astype('datetime64[Y]').astype(int) + 1970

def getMonth(t):
    return int(t.astype('datetime64[M]').astype(int)%12+1)

def getDay(t):
    return int((t - t.astype('datetime64[M]'))/ np.timedelta64(1, 'D')) + 1

def getTwoDigitYear(t):
    return getYear(t)%100

def getDOY(t):
  year=t.astype('datetime64[Y]')
  dayOfYear=((t-year)/np.timedelta64(1,'D')+1).astype(np.int64)
  return dayOfYear





if __name__=="__main__":
    t=np.datetime64('2021-05-30T23:45:00') 
    
    print("Time: ",t)
    print("Seconds of day:" , getSecsOfDay(t))
    #dayOfWeek=(t.astype('datetime64[D]').view('int64') - 3) % 7
    print("GPS week", getGpsWeek(t))
    print("Day of GPS week:", getDayOfWeek(t))
    print("Day of year:",getDayOfYear(t))
    print("Seconds of week:",getSecsOfWeek(t))
    print("Year with two digits:",getTwoDigitYear(t))
    print("Day:", getDay(t))
    print("Month:", getMonth(t))
    print("Year:", getYear(t))
    print("Julian:", getJulianDay(t))
