import numpy as np
import os
#import matplotlib.pyplot as plt
#from _pickle import dump
#from _pickle import load
''' FFTlenght as N
def per(x, FFTlenght):
    N = len(x)
    X = np.fft.fft(x, N)
    PerX = ((abs(X) ** 2) / N)
    return PerX
'''

'''
# Plot fft of a sigal, just for a visual comparison
def plot_fft(y, n, fA):
    fig = plt.figure()
    time_step = 1/fA
    Y = np.fft.fft(y, n)
    freq = np.fft.fftfreq(len(Y), time_step)
    plt.stem(freq, abs(Y))
    plt.show
    return fig
'''

# x,y = function.all.signalfromfile('out.txt')
def signalfromfile(ifile):
    with open(ifile, 'r') as f:
        lines = f.readlines()
        f.close()
    xi = []
    yi = []
    for i in lines:
        p = i.split()
        xi.append(p[0])
        yi.append(p[1])
    xa = np.array(xi).astype(np.int)
    ya = np.array(yi)
    
    #x = np.asfarray(xa,np.int_) # Still comes out as a float??
    y = np.asfarray(ya,complex)
    return (xa,y)


# Read in standard deviation
def readinstd(ifile):
    with open(ifile, 'r') as f:
        lines = f.readlines()
        f.close()
    xi = []
    for i in lines:
        p = i.split()
        xi.append(p)
    xa = np.array(xi).astype(np.float)
    return (xa)


# Generate a frequency vector of size n based on mean and std
def randfgen(mean,stand_deviation, n):
    randstate = np.random.get_state()
    freqvec = np.random.normal(mean, stand_deviation, n)
    freqvec = np.array(freqvec)
    return freqvec, randstate

def randphasegen(n):
    phi = np.random.uniform(0,2*np.pi,n)
    phi = np.array(phi)
    return phi

#Calculate power of signal (periodic)
def powersignal(x):
    p = (1/(2 * len(x) +1)) * np.sum(abs(x)**2)
    return p


# https://stackoverflow.com/questions/14058340/adding-noise-to-a-signal-in-python
# target_snr_db = 20
# noise = awgn_gen(SIGNAL, 20, 0)
# durch wurzel2 wegen komplex zeigerlaenge wegen leistung
def awgn_gen(x, snr_db, noise_mean):
    # Power of x in dB
    samples = len(x)
    x_power = powersignal(x)
    x_power_db = 10 * np.log10(x_power)
    noise_power_db = x_power_db - snr_db
    noise_power = 10 ** (noise_power_db / 10)
    randstate_noise_r = np.random.get_state()
    noise_r = np.random.normal(noise_mean, np.sqrt(noise_power), samples)
    randstate_noise_i = np.random.get_state()
    noise_i = np.random.normal(noise_mean, np.sqrt(noise_power), samples)
    noise_signal = (noise_r + 1j * noise_i)/np.sqrt(2)
    return noise_signal, randstate_noise_r, randstate_noise_i
    
    
def complexexpo(amplitude, f0, fA, phi, k):
    k = np.arange(k)
    f0.shape = (len(f0), 1)  # Vector
    if type(phi) == np.ndarray:
        phi.shape = (len(phi), 1)
    x = np.exp(1j * (( 2 * np.pi * np.divide(f0, fA) * k) + phi))
    return k, x

# Einheitskreis!!!
def cyclicdiff(fa,fb):
	df = np.arctan2(np.sin(2*np.pi*(fa-fb)),np.cos(2*np.pi*(fa-fb)))/(2*np.pi)
	df = abs(df)
	return df

def writetofile(ofile, k, x):
    with open(ofile, 'w') as f:
        f.truncate(0)
        for i in range(len(k)):
            if i == (len(k)-1):
                f.write(f"{k[i]} {x[i]}")
            else:
                f. write(f"{k[i]} {x[i]}\n")


def simugen_signal(stdfile, sensor_temp, sensor_count, freq_mean, amplitude, fA, phi, kk, snr_db, noise_mean):
    # Generate a a frequency for each sensor (normal distributed around zero) at temperature
    std_f = readinstd(stdfile)

    # Get the location of the first matching temperature
    # FIXME (what to do with other occurances?)
    temploc = np.min(np.argwhere(std_f[:,1] == sensor_temp))

    temp = []
    f0 = []

    f0, randstate_f0 = randfgen(freq_mean,std_f[temploc,0], sensor_count)
    f0 = np.array(f0)

    # Sort f0 from largest to smallest frequency
    #f0_sorted = f0[f0[:,0].argsort()[-sensor_count:][::-1]]
    f0_sorted = f0[f0.argsort()]
    f0_sorted = np.squeeze(f0_sorted)


    # Generates a complex signal for each frequency
    k, x = complexexpo(amplitude, f0, fA, phi, kk)

    combinedsignal = np.zeros(len(x[0]))

    # Adds all signals in x together
    #for c in range(len(x)):
    #    combinedsignal = combinedsignal + x[c]
    combinedsignal = x.sum(axis=0)

    # Adds noise to our signal
    noise_signal, randstate_noise_r, randstate_noise_i = awgn_gen(combinedsignal, snr_db, noise_mean)
    combinedsignal = combinedsignal + noise_signal
    return f0_sorted, randstate_f0, randstate_noise_r, randstate_noise_i, k, combinedsignal


def simugen_fileless(freq_std, sensor_temp, sensor_count, freq_mean, amplitude, fA, phi, kk, snr_db, noise_mean):
    # Generate a a frequency for each sensor (normal distributed around zero) at temperature
    f0 = []
    f0, randstate_f0 = randfgen(freq_mean,freq_std, sensor_count)
    f0 = np.array(f0)
    #if (phi == 0):
    phi = randphasegen(sensor_count)
        
        
    # Sort f0 from largest to smallest frequency
    #f0_sorted = f0[f0[:,0].argsort()[-sensor_count:][::-1]]
    f0_sorted = f0[f0.argsort()]
    f0_sorted = np.squeeze(f0_sorted)


    # Generates a complex signal for each frequency
    k, x = complexexpo(amplitude, f0, fA, phi, kk)

    combinedsignal = np.zeros(len(x[0]))

    # Adds all signals in x together
    #for c in range(len(x)):
    #    combinedsignal = combinedsignal + x[c]
    combinedsignal = x.sum(axis=0)

    # Adds noise to our signal
    noise_signal, randstate_noise_r, randstate_noise_i = awgn_gen(combinedsignal, snr_db, noise_mean)
    combinedsignal = combinedsignal + noise_signal
    return f0_sorted, randstate_f0, randstate_noise_r, randstate_noise_i, k, combinedsignal


def namegen(sim_nr, kk, sensor_count):
    simucount = '{0:0>3}'.format(sim_nr)
    filename_rand_f0 = "k_" + str(kk) + "_N_" + str(sensor_count) + "/state_f0__k_" + str(kk) + "_N_" + str(sensor_count) + "_[" + simucount + "].bin" 
    filename_rand_noise_r = "k_" + str(kk) + "_N_" + str(sensor_count) + "/state_noise_R__k_" + str(kk) + "_N_" + str(sensor_count) + "_[" + simucount + "].bin" 
    filename_rand_noise_i = "k_" + str(kk) + "_N_" + str(sensor_count) + "/state_noise_I__k_" + str(kk) + "_N_" + str(sensor_count) + "_[" + simucount + "].bin"
    return filename_rand_f0, filename_rand_noise_r, filename_rand_noise_i
    
    
# https://stackoverflow.com/questions/6773584/how-is-pythons-glob-glob-ordered
# Key for .sort function to ignore file endings
def sortKeyFunc(s):
    return int(os.path.basename(s)[:-4])
    

def zeropadding(x,M):
    M=int(M)
    x = np.append(x,np.zeros(M))
    return x
    

