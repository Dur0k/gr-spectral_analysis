import numpy as np
import function.spectral_analysis as sa
from function.constants import error_nan
import scipy
from datetime import datetime

def freq_calc(x,poly,M,fA,sensor_count,window='boxcar',thres=0.001,min_dist=10):
    # Calculate frequencies of signal x with periodogram, if M>1 use oversampling
    Mx = int(M*len(x))
    if (Mx > len(x)):
        x = np.append(x,np.zeros(Mx-len(x)))
        nfft = len(x)
    else:
        Mx = int(M*len(x))
        nfft = Mx

    f_per,_ = sa.periodogram_freq(x, fA, window, nfft, sensor_count, thres=0.001, min_dist=10, return_onesided=False, scaling='spectrum')
    f_sorted = f_per[f_per.argsort()]
    pp = np.array(poly)
    # Shift polynomials by calculated frequencies
    pp[:,3] = pp[:,3] - f_sorted

    # For all shifted polynomials calculate roots
    roots = np.empty((pp.shape[0],1))
    roots[:] = np.nan
    for i in range(0,pp.shape[0]):
        tmp = np.roots(pp[i])
        tmp = np.where(np.iscomplex(tmp),np.nan,tmp)
        tmp = np.where(tmp>40,np.nan,tmp)
        tmp = np.where(tmp<0,np.nan,tmp)
        # If all entries in tmp are nan then save a nan to roots
        if (np.isnan(tmp).all() == True):
            roots[i] = np.nan
        # Otherwise if a Number exists save it to roots
        elif ((~np.isnan(tmp)).any() == True):
            roots[i] = tmp[np.where(~np.isnan(tmp))]

    return roots, f_sorted

