#%%
from logging import log
import numpy as np
import math
import matplotlib.pyplot as pl
from numpy.core.multiarray import arange
import pandas as pd
import csv as csv
from random import seed
from random import randint
#%%

Tilt =0
Deinclanation =0
i=1


#%%
# hour angle 
Hour_angle= []
for i in np.arange(6,18,0.1):
     Hour_angle.append (15*(i-12))
hour=[]
x= []
y= []
for i in np.arange(6,18,0.1):
     hour.append (i)
for i in np.arange(6,18,0.1):
     hour.append (i)   

#%%
# elevation
Alt=np.arcsin(np.cos(np.deg2rad(Hour_angle)))
#pl.plot(hour,Alt)
#pl.show()
# %%
# solar radiation
Lat=0
Height=0
Peak_solar_cons=990.274+5.867*Lat-0.14927*(Lat**2)+0.033639*Height
correction=0.981
Io=Peak_solar_cons*correction
Sol_rad=Peak_solar_cons*np.cos(np.deg2rad(Hour_angle))

#%%
'''
pl.plot(Hour_angle,Sol_rad)
pl.ylabel('Solar Radiation (W/M^2)')
pl.xlabel('Hour Angle(Degrees)')
'''


#%%
P_STC=200
irad_coeff=Sol_rad/1000
T=[]
'''
with open('data.csv', mode ='r')as file:
     csvfile= csv.reader(file)
     print(csvfile)
'''

"""
mod_temp= [0]
T= [ 20.0, 21.0, 21.0, 21.0, 21.0, 22.0, 23.0, 25.0, 23.0, 25.0,
     23.0, 23.0, 22.0, 23.0, 23.0, 22.0, 21.0, 20.0, 20.0, 19.0,
     19.0, 17.0, 16.0, 15.0, 15.0, 15.0, 15.0
]
"""
seed (101)
for i in np.arange(15, 25, 0.083):
     T.append (randint(15,25))

# 1+k1ln(G')+k2ln(G')2 +k3T'm +k4T'mln(G') +k5T'mln(G')2 +k6T'm2

K = np.array([0.017237, 0.040465,-0.004702, 0.000149 ,0.000170 ,0.000005])
Solar_pwr = lambda T : irad_coeff*(P_STC + K[0]*np.log(irad_coeff) + K[1]*np.log(irad_coeff)**2 + K[3]*T+K[4]*T*np.log(irad_coeff) + K[4]*T*np.log(irad_coeff)**2 + K[5]*T**2) # T is temperature
Solar_pwr2=[]
for i in T:
     Solar_pwr = lambda i : irad_coeff*(P_STC + K[0]*np.log(irad_coeff) + K[1]*np.log(irad_coeff)**2 + K[3]*i+K[4]*i*np.log(irad_coeff) + K[4]*i*np.log(irad_coeff)**2 + K[5]*i**2) # T is temperature
     Solar_pwr2.append (Solar_pwr(i))     

#Solar_pwr = lambda T : irad_coeff*(P_STC + K[0]*np.log(irad_coeff) + K[1]*np.log(irad_coeff)**2 + K[3]*T+K[4]*T*np.log(irad_coeff) + K[4]*T*np.log(irad_coeff)**2 + K[5]*T**2) # T is temperature
#Solar_pwr(12)

#Solar_pwr= irad_coeff*(P_STC+K[0]*np.log(irad_coeff) + K[1]*np.log(irad_coeff)**2)



# 3. incorporate temperature as a parameter
# 4. grab JHB hourly temperature data over a day
#         a. find data online
#         b. build own database from a API

#%%

from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation 
import matplotlib.path as mpath 
# initializing a figure in 
# which the graph will be plotted
x_circle=[]
y_circle=[]
for i in np.arange(6, 18, 0.1):
    x_circle.append( 90*np.cos(np.radians(15*(i-12))))
    y_circle.append( 12+6*np.sin(np.radians(15*(i-12))))

colors = [ 'yellow']
star = mpath.Path.unit_regular_star(6)

fig = plt.figure() 
dots=[]
fig.set_size_inches(20, 20, True)

ax  = fig.add_subplot(1,2,1) 
ax2 = fig.add_subplot(1,2,2)

def animate(i):
     x=[]
     y=[]
     x2=[]
     y2=[]
     x = Solar_pwr2[0:i]
     y = hour[0:i]
     x2=y_circle[1,0:i]
     y2=x_circle[0:i]
     ax.clear()
     ax.plot(y,x)
     ax2.clear()
     ax2.plot(x2,y2 , 'y', linestyle='none', marker=star, markersize=25)  
     ax2.plot(12,0, 'b', linestyle='none', marker='s', markersize=25)  


animate = FuncAnimation(fig, func=animate, frames= 360, interval=100 )


   
animate.save('animation.gif', 
          writer = 'ffmpeg', fps = 30)
pl.show()
