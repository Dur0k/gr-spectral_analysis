'''
A collection of spectral estimation functions with parts from Parametrix Lib for Python 
https://github.com/vincentchoqueuse/parametrix
Peakutils
https://bitbucket.org/lucashnegri/peakutils/src/master/
and an autocorrelation matrix by xialulee
http://blog.sina.com.cn/s/blog_4513dde60100o6na.html
'''
import numpy as np
from scipy import signal as sg
from numpy import linalg as lg
import scipy
import itertools
from scipy import angle, arange, atleast_1d,\
     complex128, conjugate, convolve,\
     exp, mat, pi, randn, zeros
from numpy.matlib import repmat
import function.peakutils

# Estimate frequencies of signal x with scipy periodogram and the peak finding algorithm peakutils
# https://bitbucket.org/lucashnegri/peakutils/src/master/
def periodogram_freq(x, fA, window, nfft, sensor_count, thres, min_dist, return_onesided=False, scaling='spectrum'):
    f, Pxx_den = sg.periodogram(x, fA, window, nfft, return_onesided=return_onesided, scaling=scaling)
    # Due to peakutils ignoring the 0 frequency, the frequency vector is cyclic elongated by inserting the last frequency of the matrix in the front, to shift the index of the 0 frequency
    #f_cyc = np.insert(f,0,f[len(f)-1])
    #Pxx_den_cyc = np.insert(Pxx_den,0,Pxx_den[len(f)-1])
    peaks = function.peakutils.indexes(Pxx_den_cyc, thres, min_dist)
    peaks_zero = []
    # Set found peaks to zero
    peaks_zero = np.zeros(Pxx_den_cyc.shape)
    peaks_zero[:] = Pxx_den_cyc
    peaks_zero[peaks] = 0

    # Sort the peaks by height with index
    peak_sorting = np.vstack((f_cyc,peaks_zero))
    #
    #high = np.flip(np.argsort(peak_sorting[1]),axis=0)
    # Ignore the first inserted freq and shift all indices by one
    high = np.flip(np.argsort(peak_sorting[1][1:len(peak_sorting[1])]),axis=0) +1
    # Add additional peaks until sensor_count is reached
    index = 0
    failure_vec = np.zeros(len(peaks))
    while (len(peaks) < sensor_count):
        #peaks = np.append(peaks, int(peaks_zero[high[index]]))
        peaks = np.append(peaks, int(high[index]))
        failure_vec = np.append(failure_vec, 1)
        index = index + 1
    while (len(peaks) > sensor_count):
        peaks = np.delete(peaks,len(peaks)-1,0)
        failure_vec = np.delete(failure_vec, len(peaks)-1, 0)
        
    f_per = f_cyc[peaks]
    return f_per, failure_vec


#http://blog.sina.com.cn/s/blog_4513dde60100o6na.html
def Rxx(x, m=None):
    '''Estimate autocorrelation matrix of vector x
    x: signal vector;
    m: size of Rxx;
    return value: autocorrelation matrix
    '''
    N = len(x)
    if m==None:
        m = N
    #elif m>N:
    #    m=int(m)
    #    #x = np.append(np.zeros(m//2),x)
    #    x = np.append(x,np.zeros(m))
    #    N = len(x)
    temp = mat(arange(0, m))
    # generate a indices matrix, as
    # 0 -1 -2 -3 ...
    # 1  0 -1 -2 ...
    # 2  1  0 -1 ...
    # 3  2  1  0 ...
    # ...
    indices = repmat(temp.T, 1, m) - repmat(temp, m, 1)
    # calcuate samples of autocorrelation functions using convolution
    acsamples = convolve(x, conjugate(x[::-1]))
    # using autocorrelation samples and indices matrix to create Rxx
    # Rxx =
    #   r[ 0] r[-1] r[-2] r[-3] ...
    #   r[ 1] r[ 0] r[-1] r[-2] ...
    #   r[ 2] r[ 1] r[ 0] r[-1] ...
    #   r[ 3] r[ 2] r[ 1] r[ 0] ...
    #   ...
    return acsamples[indices + N - 1] / N


def subspace_estimator(R,L,technique="esprit"):
    
    M=R.shape[0]
    U,D,V=lg.svd(R)
    
    if technique=="root_music":
        
        #construct matrix P
        G=np.matrix(U[:,L:])
        P=G*G.H
        
        #construct polynomial Q
        Q=0j*np.zeros(2*M-1)
        #Extract the sum in each diagonal
        for (idx,val) in enumerate(range(M-1,-M,-1)):
            diag=np.diag(P,val)
            Q[idx]=np.sum(diag)
        
        #Compute the roots
        roots=np.roots(Q)
        
        #Keep the roots with radii <1 and with non zero imaginary part
        roots=np.extract(np.abs(roots)<1,roots)
        roots=np.extract(np.imag(roots) != 0,roots)
        
        #Find the L roots closest to the unit circle
        distance_from_circle=np.abs(np.abs(roots)-1)
        index_sort=np.argsort(distance_from_circle)
        component_roots=roots[index_sort[:L]]
        
        w=-np.angle(component_roots)
    
    if technique in ["esprit","esprit_TLS"]:
        
        S=np.matrix(U[:,:L])
        
        #Remove last and fist row
        S1=S[:-1,:]
        S2=S[1:,:]
        
        #Compute matrix Phi (Performance Analysis of the Total Least Squares
        #ESPRIT Algorithm
        if technique=="esprit":  #EQ14
            Phi=lg.pinv(S1)*S2
        
        if technique=="esprit_TLS": #EQ12
            m,n=S1.shape
            m,p=S2.shape
            E=np.matrix(np.hstack((S1,S2)))
            RE=E.H*E
            
            V_TLS,L_TLS,V2_TLS=lg.svd(RE)
            V12 = V_TLS[:n,n:]
            V22 = V_TLS[n:,n:]
            Phi=-V12*lg.inv(V22)
        
        V,U=lg.eig(Phi)
        w=-np.angle(V)

    return np.sort(w)
    

