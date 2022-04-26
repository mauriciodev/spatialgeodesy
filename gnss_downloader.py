try:
    from spatialgeodesy.gnsstime import *
except:
    from gnsstime import *
import os
from zipfile import ZipFile
import urllib.request
from io import StringIO
import pandas as pd
import re

class gnssdownloader:
    def __init__(self,folder=''):
        if folder=='':
            self.datafolder=self.datafolder=os.path.join(os.getcwd(),'gnssdata')
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

        


if __name__=="__main__":
    gd=gnssdownloader()
    epoch=np.datetime64('2021-08-30T23:45:00') 
    gd.getBRDC(epoch)
    fname=gd.getSP3(epoch)
    fname=gd.getRBMC(epoch,"RJNI",2)
    df=gd.getITRF_df()
    print(df)
