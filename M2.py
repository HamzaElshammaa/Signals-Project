
'song'
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft
import math

'creating an array for time, time of song is 3 seconds, sample size is 2*12*1024'
time = np.linspace(0, 3, 2 * 12 * 1024)

'left and right array contain frequencies for piano notes form octaves'
right = np.array([261.63, 293.66974569918125, 329.63314428399565, 349.2341510465061, 392.0020805232462, 440.00745824565865, 493.89167285382297, 261.63])
left = np.zeros_like(right)

't1 contains note begining and t2 note delay'
t1 = np.array([0,0.4,0.8,1.2,1.6,2.0,2.4,3.2,3.6,4.0,4.4,4.8,5.2,5.6])
t2 = np.array([0.3,0.7,1.1,1.5,1.9,2.3,2.7,3.5,3.9,4.3,4.7,5.1,5.5,5.9])
'8 is the num of frequencies'
Num = 8
count = 0
sum1 = 0

while count < Num:
    Freqr = right[count]
    freql = left[count]
    tp = t1[count]
    Tt = t2[count]
    Note1 = np.sin(2 * np.pi * Freqr * time)
    Note2 = np.sin(2 * np.pi * freql * time)
    sum1 = sum1 + (Note1 + Note2) * ((time >= tp) & (time <= (Tt)))
    count = count + 1

song = sum1
'Nomber of samples'
N = 3*1024
F = np.linspace(0,512,int(N/2))
'Convert song from time domain to frequency domain'
song_f = fft(song)
song_f = 2 / N * np.abs(song_f[0:np.int(N/2)])

'Generate 2 random noise signals'
fn1 = np.random.randint(0, 512, 1)
fn2 = np.random.randint(0, 512, 1)
noise = np.sin(2 * np.pi * fn1 * time) + np.sin(2 * np.pi * fn2 * time)

'Add noise to the song'
song_n = song + noise

' Convert the noisy song to the frequency domain'
song_n_f = fft(song_n)
song_n_f = 2 / N * np.abs(song_n_f[0:np.int(N/2)])

' Filtering'
max1 = 0
max2 = 0
maxIndex1 = -1
maxIndex2 = -1
i = 0

while i < len(song_n_f) - 1:
    if song_n_f[i] > max1:
        max2 = max1
        maxIndex2 = maxIndex1
        max1 = song_n_f[i]
        maxIndex1 = i
    elif song_n_f[i] > max2:
        max2 = song_n_f[i]
        maxIndex2 = i
    i=i+1
    
    
songFiltered = song_n -(np.sin(2*np.pi*int(F[maxIndex1])*time) + np.sin(2*np.pi*int(F[maxIndex2])*time))
sd.play(songFiltered , 4*1024)
#convert filtered song to frequency domain
songFiltered_f=fft(songFiltered)
songFiltered_f=2/N*np.abs(songFiltered_f[0:np.int(N/2)])
'plt.figure creates a graph page'
'plotting in time domain'
plt.figure()
plt.subplot(3,1,1)
plt.plot(time,song)
plt.subplot(3,1,2)
plt.plot(time,song_n)
plt.subplot(3,1,3)
plt.plot(time,songFiltered)
#plot frequency
'plotting in frequency domain'
plt.figure()
plt.subplot(3,1,1)
plt.plot(F,song_f)
plt.subplot(3,1,2)
plt.plot(F,song_n_f)
plt.subplot(3,1,3)
plt.plot(F,songFiltered_f)
