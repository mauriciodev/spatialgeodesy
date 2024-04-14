try:
    from spatialgeodesy.gnsstime import *
except:
    from gnsstime import *
import os, io
from zipfile import ZipFile
import gzip
import urllib.request
from io import StringIO
import pandas as pd
import re
import subprocess

class gnssdownloader:
    def __init__(self,folder=''):
        if folder=='':
            self.datafolder=os.path.join(os.getcwd(),'gnssdata')
        else:
            self.datafolder=os.path.join(folder,'gnssdata')
        self.checkFolder(self.datafolder)

    def checkFolder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
    def getBRDC(self,t):
        doy=getDayOfYear(t)
        year=np.datetime64(t,'Y')#t.astype('datetime64[Y]')
        baseurl="https://igs.bkg.bund.de/root_ftp/IGS/BRDC/{0}/{1:03}/BRDM00DLR_S_{0}{1:03}0000_01D_MN.rnx.gz".format(str(year),doy)
        local_filename = baseurl.split('/')[-1]
        print("Downloading from BKG ", baseurl)
        self.brdcfolder=os.path.join(self.datafolder,"BRDC")
        self.checkFolder(self.brdcfolder)
        file_name=os.path.join(self.brdcfolder,local_filename)
        if not os.path.exists(file_name):
            urllib.request.urlretrieve(baseurl, file_name)
        print("Saved ",file_name)        
        return file_name


    def getSP3(self,t):
        gpsWeek=getGpsWeek(t)
        dayOfWeek=getDayOfWeek(t)
        baseurl="https://igs.bkg.bund.de/root_ftp/IGS/products/orbits/{0}/cod{0:04}{1}.eph_r.Z".format(gpsWeek,dayOfWeek)
        local_filename = baseurl.split('/')[-1]
        print("Downloading from BKG ", baseurl)
        self.sp3folder=os.path.join(self.datafolder,"SP3")
        self.checkFolder(self.sp3folder)
        file_name=os.path.join(self.sp3folder,local_filename)
        if not os.path.exists(file_name):
            urllib.request.urlretrieve(baseurl, file_name)
        print("Saved ",local_filename)
        return file_name

    #precise_orbits_url="https://igs.bkg.bund.de/root_ftp/IGS/products/orbits/{0}/cod{0:04}{1}.eph_r.Z".format(gpsWeek,dayOfWeek)

    def getRBMC(self,t,station, rinexversion=3):
        doy=getDOY(t)
        year=np.datetime64(t,'Y')#t.astype('datetime64[Y]')
        if rinexversion==3:
            baseurl="https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados_RINEX3/{0}/{1:03}/{2}00BRA_R_{0}{1:03}0000_01D_15S_MO.crx.gz".format(str(year),doy,station)
        else:
            baseurl="https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/{0}/{1:03}/{2}{1}1.zip".format(str(year),doy,station.lower() )
        local_filename = baseurl.split('/')[-1]
        print("Downloading from IBGE ", baseurl)
        if not os.path.exists(local_filename):
            urllib.request.urlretrieve(baseurl, local_filename)
        print("Saved ",local_filename)
        print("Unzipping")
        with ZipFile(local_filename, 'r') as zipObj:
            outdir=local_filename.split('.')[0]
            zipObj.extractall(outdir)
            files=zipObj.namelist()
            files = [ outdir+ "/"+ sub for sub in files]
        return files
    
    def getITRF_df(self):
        baseurl="https://itrf.ign.fr/docs/solutions/itrf2020/Transfo-ITRF2020_TRFs.txt"
        print("Downloading from IGN ", baseurl)
        local_filename = baseurl.split('/')[-1]
        file_name=os.path.join(self.datafolder,local_filename)
        if not os.path.exists(file_name):
            urllib.request.urlretrieve(baseurl, file_name)
        itrfFile=open(file_name)
        itrfData = itrfFile.readlines()
        itrfFile.close()
        l=[]
        lastLine=''
        for line in itrfData:
            line=line.strip()
            if line.startswith("rates") or line.startswith("RATES"):
                l.append(lastLine+" "+line)
            elif line.startswith("ITRF") or line.startswith("SOLUTION"):
                lastLine=line
        sio=StringIO('\n'.join(l))
        itrfdf=pd.read_csv(sio,delim_whitespace=True)
        return itrfdf

    def downloadBias(self,doy,year,outdir='.'):
        baseurl="ftp://igs.ign.fr/pub/igs/products/mgex/dcb/{year}/CAS0MGXRAP_{year}{0:03}0000_01D_01D_DCB.BSX.gz".format(doy,year=year)
        #wget -r "ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/bias/2014/"
        #baseurl="ftps://gdc.cddis.eosdis.nasa.gov/gnss/products/bias/{year}/CAS0MGXRAP_{year}{0:03}0000_01D_01D_DCB.BSX.gz".format(doy,year=year)
        #print(baseurl)
        local_filename = baseurl.split('/')[-1]
        local_filename=os.path.join(outdir,local_filename)
        
        if not os.path.exists(local_filename):
            print("Downloading ", baseurl)
            urllib.request.urlretrieve(baseurl, local_filename)
            #subprocess.run(f'wget \"{baseurl}\" -O {local_filename}',shell=True)
            print("Saved ",local_filename)
            #gunzip $local_filename -f
        with gzip.open(local_filename, 'rt') as f:
            lines=f.read()
        if lines=='':
            return None
        lines=' '+re.search('\*BIAS(.+)\n-BIAS', lines, flags=re.DOTALL).group(0)[1:-5]
        data = io.StringIO(lines)
        df=pd.read_fwf(data, infer_nrows=1)
        return df

    def getSSN(self):
        ssndf=pd.read_json("https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json")
        return ssndf
        

if __name__=="__main__":
    gd=gnssdownloader()
    #epoch=np.datetime64('2021-08-30T23:45:00') 
    #gd.getBRDC(epoch)
    #fname=gd.getSP3(epoch)
    #fname=gd.getRBMC(epoch,"RJNI",2)
    #df=gd.getITRF_df()
    #print(df)
    for year in range(2013,2020):
        for doy in range(1,365, 50):
            outdir='dcb' 
            #outdir='dcb' 
            station='BRAZ'
            df=gd.downloadBias(doy,year, outdir=outdir)
            try:
                pass
            except:
                print(f"Day {doy} year {year} not found.")
                continue
            if not df is None:
                if "SITE" in df.columns:
                    station_row=df[(df["SITE"]==station)]
                elif "STATION__" in df.columns:
                    station_row=df[(df["STATION__"]==station)]
                if len(station_row)>0:
                    #print(station_row)
                    print(f"Found {station} in {doy}/{year} {outdir}")
                    biasdf=station_row[(station_row["OBS1"]=="C1C") & (station_row["OBS2"]=="C2W")]
                    biasdf2=station_row[(station_row["OBS1"]=="C2W") & (station_row["OBS2"]=="C2X")]
                    if len(biasdf)>0 and len(biasdf2)>0:
                        print("found DCB")
    #print(df)
