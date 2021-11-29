import numpy as np

class ellipsoid:
  def __init__(self,a=0,denf=0):
    self.a=a
    self.denf=denf
  def setGRS80(self):
    self.a=6378137
    self.denf=298.2572221
  def b(self):
    return self.a*(1-1/self.denf)
  def a(self):
    return a
  def f(self):
    return 1/denf
  def e(self):
    e=np.sqrt(1- self.b()**2/(self.a**2))
    return e
  def e2(self):
    e2=np.sqrt(self.a**2/self.b()**2- 1)
    return e2
  def N(self,lat):
    aux=self.e()*np.sin(lat)
    N=self.a/np.sqrt(1-aux*aux)
    return N
  def M(self,lat):
    e=self.e
    M=a*(1-e**2)/(1-e**2 *np.sin(lat)*np.sin(lat))**1.5
    return M
  def xyz2latlon(self,xyz):
    xyz=np.array(inputXYZ)
    lon=np.arctan(xyz[1]/xyz[0]);
    p=np.sqrt(xyz[0]*xyz[0]+xyz[1]*xyz[1]);
    e=self.e();
    e2=self.e2();
    b=self.b();
    u=np.arctan(xyz[2]*a/(p*b));
    lat=np.arctan((xyz[2]+e2*e2*b*np.sin(u)**3)/(p-e*e*a*np.cos(u)**3));
    N0=a/np.sqrt(1-e*e*np.sin(lat)*np.sin(lat));
    h=p/np.cos(lat)-N0;
    return np.array([lon*180/np.pi,lat*180/np.pi, h])
  def xyz2latlonIter(self, xyz):
    lon=np.arctan(xyz[1]/xyz[0]);
    p=np.sqrt(xyz[0]*xyz[0]+xyz[1]*xyz[1]);
    e=self.e();
    error=1;
    h=0; N0=1; lat0=1000;
    while (error>1e-10):
      lat1=np.arctan(xyz[2]/p/(1-e*e*N0/(N0+h)));
      N0=a/np.sqrt(1-e*e*np.sin(lat1)*np.sin(lat1));
      h=p/np.cos(lat1)-N0;
      error=abs(lat1-lat0);
      lat0=lat1;
    return np.array([lon*180/np.pi,lat*180/np.pi, h])
  def latlon2xyz(self,lon,lat,h):
    e=self.e();
    N=self.N(lat);
    x=(N+h)*np.cos(lat)*np.cos(lon);
    y=(N+h)*np.cos(lat)*np.sin(lon);
    z=(N*(1-e*e)+h)*np.sin(lat);
    return np.array([x,y,z])

if __name__=="__main__":
    grs80=ellipsoid()
    grs80.setGRS80()
    print(grs80.a)
