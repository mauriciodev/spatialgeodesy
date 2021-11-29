import numpy as np

class ellipsoid:
  def __init__(self,a=0,denf=0):
    self.a=a
    self.denf=denf
    self.setGRS80()
    
  def setGRS80(self):
    self.a=6378137
    self.denf=298.2572221
    self.prepare()
  def prepare(self):
    self.b=self.a*(1-1/self.denf)
    self.e=np.sqrt(1- self.b**2/(self.a**2))
    self.e2=np.sqrt(self.a**2/self.b**2- 1)
  def f(self):
    return 1/denf

  def N(self,lat):
    aux=self.e*np.sin(lat)
    N=self.a/np.sqrt(1-aux*aux)
    return N
  def M(self,lat):
    e=self.e
    M=a*(1-e**2)/(1-e**2 *np.sin(lat)*np.sin(lat))**1.5
    return M
  def xyz2lonlath(self,xyz):
    xyz=np.array(xyz)
    lon=np.arctan(xyz[1]/xyz[0]);
    p=np.sqrt(xyz[0]*xyz[0]+xyz[1]*xyz[1]);
    e=self.e;
    e2=self.e2;
    b=self.b;
    u=np.arctan(xyz[2]*self.a/(p*b));
    lat=np.arctan((xyz[2]+e2*e2*b*np.sin(u)**3)/(p-e*e*self.a*np.cos(u)**3));
    N0=self.a/np.sqrt(1-e*e*np.sin(lat)*np.sin(lat));
    h=p/np.cos(lat)-N0;
    return np.array([lon*180/np.pi,lat*180/np.pi, h])
  def xyz2lonlathIter(self, xyz):
    lon=np.arctan(xyz[1]/xyz[0]);
    p=np.sqrt(xyz[0]*xyz[0]+xyz[1]*xyz[1]);
    e=self.e;
    error=1;
    h=0; N0=1; lat0=1000;
    while (error>1e-10):
      lat1=np.arctan(xyz[2]/p/(1-e*e*N0/(N0+h)));
      N0=self.a/np.sqrt(1-e*e*np.sin(lat1)*np.sin(lat1));
      h=p/np.cos(lat1)-N0;
      error=abs(lat1-lat0);
      lat0=lat1;
    return np.array([lon*180/np.pi,lat0*180/np.pi, h])
  def lonlath2xyz(self,lonlath):
    lat=lonlath[1]/180*np.pi
    lon=lonlath[0]/180*np.pi
    h=lonlath[2]
    e=self.e;
    N=self.N(lat);
    x=(N+h)*np.cos(lat)*np.cos(lon);
    y=(N+h)*np.cos(lat)*np.sin(lon);
    z=(N*(1-e*e)+h)*np.sin(lat);
    return np.array([x,y,z])

if __name__=="__main__":
    grs80=ellipsoid()
    xyz=[5176588.653, -3618162.163, -887363.920 ]
    lonlath=grs80.xyz2lonlath(xyz)
    print(xyz)
    print(lonlath)
    print(grs80.xyz2lonlathIter(xyz))
    print(grs80.lonlath2xyz(lonlath))
