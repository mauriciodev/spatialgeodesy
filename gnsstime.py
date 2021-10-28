import erfa
import numpy as np
from datetime import datetime

def getMJD(t):
    return getJulianDay(t)- 2400000.5

def getJulianDay(t):
    aux=erfa.cal2jd(getYear(t),getMonth(t),getDay(t))
    return aux[0]+aux[1]

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
    year=getYear(t)
    return year.astype(int)-30

def getDOY(t):
  year=t.astype('datetime64[Y]')
  dayOfYear=((t-year)/np.timedelta64(1,'D')+1).astype(np.int64)
  return dayOfYear





if __name__=="__main__":
    t=np.datetime64('2021-05-30T23:45:00') 
    
    print("Time: ",t)
    today=t.astype('datetime64[D]')
    secsOfDay=(t-today)/ np.timedelta64(1, 's')
    print("Seconds of day:" , secsOfDay)
    print(getSecsOfDay(t))
    #dayOfWeek=(t.astype('datetime64[D]').view('int64') - 3) % 7
    gps_t0=np.datetime64('1980-01-06T00:00:00')
    gpsWeek=((t - gps_t0)/ np.timedelta64(1, 'D')/7).astype(np.int64)
    print("GPS week", gpsWeek)
    print(getGpsWeek(t))
    dayOfWeek=((t - gps_t0)/ np.timedelta64(1, 'D') % 7).astype(np.int64)
    print("Day of GPS week:", dayOfWeek)
    print(getDayOfWeek(t))
    year=t.astype('datetime64[Y]')
    dayOfYear=((t-year)/np.timedelta64(1,'D')+1).astype(np.int64)
    print("Day of year:",dayOfYear)
    print(getDayOfYear(t))
    secsOfWeek=secsOfDay+dayOfWeek*24*60*60
    print("Seconds of week:",secsOfWeek)
    twoDigitYear=year.astype(int)-30
    print("Year with two digits:",twoDigitYear)
    print("Day:", getDay(t))
    print("Month:", getMonth(t))
    print("Year:", getYear(t))
    print("Julian:", getJulianDay(t))
