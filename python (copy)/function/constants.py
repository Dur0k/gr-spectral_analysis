# Contains all constant values for plot.py
import numpy as np

# Polynomial data for sensors
#Sensor 5 data from column 14 lowest freq values
p_5=np.array([2.22769620e-02, -1.70367733e+00, -1.58914013e+01, 1.19999708e+08])
#Sensor 10 data from column 6 second highest
p_10=np.array([3.75334018e-02, -2.24642587e+00, -3.69621493e+01, 1.20001284e+08])
#Sensor 14 data from column 1 highest freq values
p_14=np.array([1.41016716e-02, -1.21260981e+00, -4.59088135e+01, 1.20001834e+08])


polynomials=np.stack((p_5,p_14,p_10),axis=0)

error_nan = np.array(['Sensor 5 is NaN','Sensor 10 is NaN','Sensor 14 is NaN'])

plot_list = np.array(['Sensor 5','Sensor 10','Sensor 14'])
