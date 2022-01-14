#%%
from logging import log
import numpy as np
import math
import matplotlib.pyplot as pl
from numpy.core.multiarray import arange, concatenate
import pandas as pd
import csv as csv
from random import seed
from random import randint
#%%

Tilt =-30      # tilt of surface
D=240
Deinclanation =-23.5*np.cos(360/365*(D+10)) # axis tilt
Lat=-30
i=1


# hour angle 
Hour_angle= []
for i in np.arange(6,18,0.1):
     Hour_angle.append (15*(i-12))

Hour_angle2= []
for i in np.arange(6,12,0.1):
     Hour_angle2.append (15*(i-12))

Hour_angle3= []
for i in np.arange(12,18,0.1):
     Hour_angle3.append (15*(i-12))


hour=[]

for i in np.arange(6,18,0.1):
     hour.append (i)

# elevation
elevation=np.arcsin(np.sin(np.deg2rad(Tilt))*np.sin(np.deg2rad(Deinclanation)) + np.cos(np.deg2rad(Tilt))*np.cos(np.deg2rad(Deinclanation))*np.cos(np.deg2rad(Hour_angle)))
#azimuth=np.arccos(np.cos(np.deg2rad(Deinclanation))*np.sin(np.deg2rad(Hour_angle)))/np.sin(elevation)
elevation2=np.arcsin(np.sin(np.deg2rad(Tilt))*np.sin(np.deg2rad(Deinclanation)) + np.cos(np.deg2rad(Tilt))*np.cos(np.deg2rad(Deinclanation))*np.cos(np.deg2rad(Hour_angle2)))
elevation3=np.arcsin(np.sin(np.deg2rad(Tilt))*np.sin(np.deg2rad(Deinclanation)) + np.cos(np.deg2rad(Tilt))*np.cos(np.deg2rad(Deinclanation))*np.cos(np.deg2rad(Hour_angle3)))

azimuth=np.arccos(np.cos(np.deg2rad(Deinclanation))*np.sin(np.deg2rad(Hour_angle2)))/np.sin(elevation2)
azimuth2=np.deg2rad(360)-np.arccos(np.cos(np.deg2rad(Deinclanation))*np.sin(np.deg2rad(Hour_angle3)))/np.sin(elevation3)

gfg = np.concatenate((azimuth, azimuth2), axis = 0)

Zenith=np.deg2rad(90)-elevation
#arbitrary angle
#ARB3=np.cos(elevation)*np.sin(Zenith)*np.cos(azimuth) + np.sin(elevation)*np.cos(Zenith)

# %%
# solar radiation

N=240               # Day
Lat=30              # latitude
Height=0            # height from sea level
correction=0
no=np.cos(2*np.pi*(N/365))
Peak_solar_cons=990.274+5.867*Lat-0.14927*(Lat**2)+0.033639*Height #Peak solar radiation on surface at particular height
correction= 1 + 0.034*no        #correction with erath orbit
Io=Peak_solar_cons*correction
Sol_rad=Io*np.cos(np.deg2rad(Hour_angle))
Sol_rad2=Io*(np.cos(np.deg2rad(Hour_angle))**2+np.sin(np.deg2rad(Hour_angle))**2)*np.cos(Zenith)
Sol_rad3=Io*np.cos(elevation)*np.sin(Zenith)*np.cos(gfg) + np.sin(elevation)*np.cos(Zenith)

Sol_rad4=Io*(np.cos(np.deg2rad(Hour_angle))**2+np.sin(np.deg2rad(Hour_angle))**2)#ideal

P_STC=200
irad_coeff=Sol_rad/1000
irad_coeff2=Sol_rad2/1000
irad_coeff3=Sol_rad3/1000
irad_coeff4=Sol_rad4/1000
T=[]

K = np.array([0.017237, 0.040465,-0.004702, 0.000149 ,0.000170 ,0.000005])
Solar_pwr = lambda T : irad_coeff*(P_STC + K[0]*np.log(irad_coeff) + K[1]*np.log(irad_coeff)**2 + K[3]*T+K[4]*T*np.log(irad_coeff) + K[4]*T*np.log(irad_coeff)**2 + K[5]*T**2) # T is temperature
Solar_pwr2 = lambda T :irad_coeff2*(P_STC + K[0]*np.log(irad_coeff2) + K[1]*np.log(irad_coeff2)**2 + K[3]*T+K[4]*T*np.log(irad_coeff2) + K[4]*T*np.log(irad_coeff2)**2 + K[5]*T**2) # T is temperature
Solar_pwr3 = lambda T :irad_coeff3*(P_STC + K[0]*np.log(irad_coeff3) + K[1]*np.log(irad_coeff3)**2 + K[3]*T+K[4]*T*np.log(irad_coeff3) + K[4]*T*np.log(irad_coeff3)**2 + K[5]*T**2) # T is temperature
Solar_pwr4 = lambda T :irad_coeff4*(P_STC + K[0]*np.log(irad_coeff4) + K[1]*np.log(irad_coeff4)**2 + K[3]*T+K[4]*T*np.log(irad_coeff4) + K[4]*T*np.log(irad_coeff4)**2 + K[5]*T**2) # T is temperature

Power=Solar_pwr(0)
Power2=Solar_pwr2(0)
Power3=Solar_pwr3(0)
Power4=Solar_pwr4(0)
pl.plot(hour,Power, label='Orginal')
pl.plot(hour,Power2, label='pitch')
pl.plot(hour,Power3, label='Parrallel facing')
pl.plot(hour,Power4, label='ideal')
pl.legend()
pl.show()

# %%
