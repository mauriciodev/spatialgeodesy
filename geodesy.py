try:
    from spatialgeodesy.ellipsoid import ellipsoid
except:
    from ellipsoid import ellipsoid

import numpy as np

def dms2dd(d,m,s):
    if d<0: sign=-1
    else: sign=1
    return sign*(abs(d)+m/60.+s/3600.)
def dd2dms(dd):
    if dd<0: sign=-1
    else: sign=1
    dd=abs(dd)
    d=np.floor(dd)
    dm=(dd-d)*60
    m=np.floor(dm)
    s=(dm-m)*60
    return sign*d,m,s 

def getElevAzi(xyzRec,xyzSat):
    #xyzSat=np.dstack([df.X.values,df.Y.values,df.Z.values])[0]
    #print(xyzSat)

    rho=np.array(xyzSat)-np.array(xyzRec) #computing the distance vector
    #print(rho)
    rho=rho/np.linalg.norm(rho) #unit vector of the distance
    #print(rho)
    grs80=ellipsoid()
    grs80.setGRS80()
    lonlath=grs80.xyz2latlon(xyzRec)
    #lonlath=erfa.gc2gd(1,xyzRec) #converting the receiver position to lon, lat, height
    lat=lonlath[1]
    lon=lonlath[0]
    rotation=np.array([
        [-sin(lon), -cos(lon)*sin(lat), cos(lon)*cos(lat) ], 
        [cos(lon), -sin(lon)*sin(lat), sin(lon)*cos(lat) ],
        [0, cos(lat),sin(lat)]
    ])
    #print(rotation)
    e=rotation[:,0]
    n=rotation[:,1]
    u=rotation[:,2]
    #print(e)
    #print(rho.dot(u))
    E=np.arcsin(rho.dot(u))
    Az=np.arctan(rho.dot(e)/rho.dot(n))
    print(E*180/np.pi,Az*180/np.pi)
    #elev_az=np.dstack([E,Az])[0]
    return E,Az
