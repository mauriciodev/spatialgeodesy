import erfa
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd 

class celestial:
    
  def getRotationMatrix(self,t):
    year = t.astype('datetime64[Y]').astype(int) + 1970
    month = t.astype('datetime64[M]').astype(int) % 12 + 1
    day = ((t - t.astype('datetime64[M]')+1)/ np.timedelta64(1, 'D')).astype(int)
    t2=t+np.timedelta64(1,'D')
    year2 = t2.astype('datetime64[Y]').astype(int) + 1970
    month2 = t2.astype('datetime64[M]').astype(int) % 12 + 1
    day2 = ((t2 - t.astype('datetime64[M]')+1)/ np.timedelta64(1, 'D')).astype(int)
    #print(year,month,day)
    df=self.getIERSBulletinB(year,month,day,year2,month2,day2)
    Xp=df.iloc[0]['x_pole[marcsec]']
    Yp=df.iloc[0]['y_pole[marcsec]']
    DUT1=df.iloc[0]['UT1-UTC[msec]']
    #print(df.keys())
    #Boletin do IERS - posicao do polo
    XP = Xp*np.pi/648000.0;#em radianos
    YP = Yp*np.pi/648000.0;
    DUT1 = DUT1*np.pi/648000.0;
    tempo = (t - t.astype('datetime64[D]')).astype(int)
    #Calendario Gregoriano para Data Juliana
    aux=erfa.cal2jd(year, month, day)
    djm0,djm=aux

    #HORA UTC (DIFERE DA HORA GPS POR 13 SEGUNDOS)
    UTC = tempo-13.0;
    UT1 = UTC + DUT1;
    TAI = UTC + 32.0; #!TEMPO ATOMICO INTERNACIONAL
    TT = TAI + 32.184; #!TEMPO TERRESTRE

    DATA1 = djm0;
    DATA2 = djm + TT/(86400.0);

    DATE2UT1 = djm + UT1/(86400.0);
    rc2t=erfa.c2t00a(DATA1, DATA2, DATA1, DATE2UT1, XP, YP)
    return rc2t

  def terrestrial2celestial(self, RT,t):
    rc2t=self.getRotationMatrix(t)
    R_celestial=erfa.trxp(rc2t, RT) 
    return R_celestial

  def celestial2terrestrial(self, RT,t):
    rc2t=self.getRotationMatrix(t)
    R_celestial=erfa.rxp(rc2t, RT)  
    return R_celestial

  def getIERSBulletinB(self,year0,month0,day0,year1,month1,day1):
    pload = {"start_year": year0,
    "start_month": month0,
    "start_day": day0,
    "end_year": year1,
    "end_month": month1,
    "end_day": day1,
    "series[]": ["Bulletin B"],
    "parameter[]": ["x_pole","y_pole","UT1-UTC"],
    "vertical": "Submit"
    }
    baseurl="https://data.iers.org/eris/eopReader/php/"
    r = requests.post(baseurl+'readeop.php',data = pload)
    soup = BeautifulSoup(r.text, 'html.parser')
    filtered = filter(lambda text: text.get('href').find("generateCSV.php")>=0, soup.find_all("a"))
    filtered=list(filtered)
    csvFileUrl=baseurl+filtered[0].get('href')
    df=pd.read_csv(csvFileUrl,delimiter=";",parse_dates={'date':['Year','Month','Day']})
    df.dropna(inplace=True,subset=['date','x_pole[marcsec]','y_pole[marcsec]'])
    return df
 
if __name__=="__main__":
    #INPUT DATA
    R_celestial=np.array([-2768.51568811, 16094.22351633, 21138.78918259])
    t=np.datetime64('2015-05-02T10:02:01')
    test=celestial()
    test.terrestrial2celestial(R_celestial,t)

    print("Celestial coordinates (km):         ",R_celestial)
    print("Expected celestial coordinates: (km)",[-2768.51569,	16094.22352,	21138.78919])
