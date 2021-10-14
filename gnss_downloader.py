import georinex as gr
import numpy as np
import xarray as xr
import requests
from datetime import datetime
from gnsstime import *
import erfa 
from unlzw import unlzw

def getBRDC(t):
  doy=getDayOfYear(t)
  year=np.datetime64(t,'Y')#t.astype('datetime64[Y]')
  baseurl="https://igs.bkg.bund.de/root_ftp/IGS/BRDC/{0}/{1:03}/BRDM00DLR_S_{0}{1:03}0000_01D_MN.rnx.gz".format(str(year),doy)
  local_filename = baseurl.split('/')[-1]
  print("Downloading from BKG ", baseurl)
  response = requests.get(baseurl)
  open(local_filename, 'wb').write(response.content)
  print("Saved ",local_filename)
  return local_filename


def getSP3(t):
  gpsWeek=getGpsWeek(t)
  dayOfWeek=getDayOfWeek(t)
  baseurl="https://igs.bkg.bund.de/root_ftp/IGS/products/orbits/{0}/cod{0:04}{1}.eph_r.Z".format(gpsWeek,dayOfWeek)
  local_filename = baseurl.split('/')[-1]
  print("Downloading from BKG ", baseurl)
  response = requests.get(baseurl)
  open(local_filename, 'wb').write(response.content)
  print("Saved ",local_filename)
  return local_filename

#precise_orbits_url="https://igs.bkg.bund.de/root_ftp/IGS/products/orbits/{0}/cod{0:04}{1}.eph_r.Z".format(gpsWeek,dayOfWeek)




with open('file.Z', 'rb') as fh:
    compressed_data = fh.read()
    uncompressed_data = unlzw(compressed_data)

if __name__=="__main__":
    epoch=np.datetime64('2021-08-30T23:45:00') 
    #getBRDC(epoch)
    getSP3(epoch)
