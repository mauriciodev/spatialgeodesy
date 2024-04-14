import re
import os
import urllib.request
import pandas as pd
import numpy as np
from io import StringIO

class itrfconverter:
    def __init__(self, datafolder=None):
        if datafolder == None:
            self.datafolder = os.path.join(os.getcwd(),'gnssdata')
        else: 
            self.datafolder = datafolder
        self.itrfdf=self.getITRF_df()
        
    def getITRF_df(self):
        baseurl="https://itrf.ign.fr/docs/solutions/itrf2020/Transfo-ITRF2020_TRFs.txt"
        file_name=os.path.join(self.datafolder,'itrf_data.txt')
        if not os.path.exists(file_name):
            print("Downloading from IGN ", baseurl)
            urllib.request.urlretrieve(baseurl, file_name)
        else: 
            print(f"File {file_name} already exists.")
        with open(file_name) as itrfFile:
            itrfData = itrfFile.read()
        #gets the solution header
        header = re.findall(r'SOLUTION.*\n', itrfData)[0].strip().split()
        #gets the rates header
        header2 = re.findall(r'RATES.*\n', itrfData)[0].strip().split() 
        #adds 'r' before the rate column names
        header2 = ['r'+x for x in header2] 
        #splits using the text ----- and ____ lines
        itrfBlock = re.split(r'[-_]+\n', itrfData)[2]
        #splits the ITRF line using "ITRF" and strips the line breaks
        itrfs = re.split(r'ITRF', itrfBlock)[1:] #first block is spaces
        itrfs = [x.replace('\n','') for x in itrfs]
        itrfdf=pd.read_csv( StringIO('\n'.join(itrfs)) ,delim_whitespace=True, names = header+header2)
        itrfdf['SOLUTION'] = itrfdf['SOLUTION'].where(itrfdf['SOLUTION'] >=100, itrfdf['SOLUTION']+1900)
        return itrfdf

    def listITRFS(self):
        return self.itrfdf.SOLUTION.to_list()
    def prepareConvertion(self,itrf,outputEpoch):
        itrfData=self.itrfdf[self.itrfdf['SOLUTION']==itrf]
        deltaRates=outputEpoch-itrfData['EPOCH'].values[0]
        #=[itrfData['Tx']+itrfData['Tx.1']*deltaRates, itrfData['Ty']+itrfData['Ty.1']*deltaRates, itrfData['Tz']+itrfData['Tz.1']*deltaRates]
        T=itrfData[['Tx','Ty','Tz']].to_numpy()[0]/1000. #meters per year
        rateT=itrfData[['rTx','rTy','rTz']].to_numpy()[0]/1000.
        self.T=T+ rateT*deltaRates
        R=itrfData[['Rx','Ry','Rz']].to_numpy()[0]/1000. #arc seconds per year
        rateR=itrfData[['rRx','rRy','rRz']].to_numpy()[0]/1000.
        R=R*rateR*deltaRates/3600 #degrees per year
        D=itrfData[['D']].to_numpy()[0]/1000. #arc seconds per year
        rateD=itrfData[['rD']].to_numpy()[0]/1000.
        self.D=D*rateD*deltaRates/10e8 #degrees per year
        self.R=np.array([[D[0], -R[2],  R[1]],
                    [R[2],  D[0], -R[0]],
                    [R[1],  R[0],  D[0]]  ])
        
    def forward(self, coords):
        I=np.identity(3)
        return np.linalg.inv(self.R+I) @ (coords-self.T)
    def backward(self,coords):
        return coords + self.T + self.R @ x 
    
    def updateCoords(self,inputCoords,inputVelocity, inputEpoch, outputEpoch):
        deltaEpoch=outputEpoch-inputEpoch
        return np.array(inputCoords)+deltaEpoch*np.array(inputVelocity)


if __name__=="__main__":
    test=itrfconverter()

    inputCoords=[4289663.4482,  -4018945.9158,  -2467135.6259]
    inputVelocity=[0,0,0]
    inputEpoch=2000.4
    inputItrf=2000
    outputEpoch=2020.62 #YEAR + DOY/365
    outputItrf=2014 # This is only working for ITRF2014 for now

    updatedCoords=test.updateCoords(inputCoords, inputVelocity, inputEpoch, outputEpoch)

    test.prepareConvertion(outputItrf,inputItrf)
    print("T",test.T)
    print("D",test.D)
    print("R",test.R)

    #xs=x + T + R @ x caso fosse 2014 para 2000
    xs=test.forward(updatedCoords)
    print ("coordenadas referenciadas ao ITRF 2014 época",outputEpoch,":",xs)
    
