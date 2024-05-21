# import matplotlib.pyplot as plt
# import numpy as np
# import sounddevice as sd
# notes = np.array([261.63,293.66974569918125,329.63314428399565,349.2341510465061,392.0020805232462,440.00745824565865,493.89167285382297])
# delay= np.array([0,0.4,0.8,1.2,1.6,2.0,2.4,3.2,3.6,4.0,4.4,4.8,5.2,5.6])
# second_delay= np.array([0.3,0.7,1.1,1.5,1.9,2.3,2.7,3.5,3.9,4.3,4.7,5.1,5.5,5.9])
# line= 0
# time = np.linspace(0, 3,12*1024)
# freq2 = 0
# for i in range(5):
#     freq1=notes[i]
#     delay1=delay[i]
#     delay2=second_delay[i]
#     line += np.reshape( (np.sin (2 * np.pi * freq1 * time))*[(time)>=delay1]*[(time)<=delay2],np.shape(time))
# plt.plot(time,line)
# sd.play(line, 3*1024)
'song'
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft
import math
'creating an array for time'
time = np.linspace(0,3,2*12*1024)
'left and right array contain frequencies for piano notes form octaves'
right = np.array([261.63,293.66974569918125,329.63314428399565,349.2341510465061,392.0020805232462,440.00745824565865,493.89167285382297,261.63])
left = np.array([0,0,0,0,0,0,0,0])
't1 contains note begining and t2 note delay'
t1 = np.array([0,0.4,0.8,1.2,1.6,2.0,2.4,3.0])
T2 = np.array([0.1,0.3,0.2,0.3,0.2,0.1,0.3,0.4])

Num=8
count=0
sum1=0
while (count<Num):
    Freqr = right[count]
    freql = left[count]
    tp = t1[count]
    Tt = T2[count]
    Note1 = np.sin(2*np.pi*Freqr*time)
    note2 = np.sin(2*np.pi*freql*time)
    sum1 = sum1 + (Note1+note2)*((time>=tp)&(time<=(tp+Tt)))
    count = count+1
song = sum1
# plt.plot(time,song)
# sd.play(song,3*1024)

'Nomber of samples'
N = 3*1024
'frequency'
F = np.linspace(0,512,int(N/2))
''''convert song from time domain to frequency domain'''
song_f=fft(song)
song_f = 2/N * np.abs(song_f [0:np.int(N/2)])

'generated 2 random noise signals and put them in a wave then '
fn1 = np.random.randint(0,512,1)
fn2 = np.random.randint(0,512,1)



noise = np.sin(2*fn1*np.pi*time)+ np.sin(2*fn2*np.pi*time)

song_n = song + noise
song_n_f=fft(song_n)

song_n_f= 2 / N * np.abs(song_n_f[0:np.int(N/2)])

'''flitering 1'''
# z = np.where(song_n_f>math.ceil(np.max(song)))
# index1 = z[0][0]
# index2 = z[0][1]
# found1 = int(F[index1])
# found2 = int(F[index2])
'''filtering 2'''
max1=0
max2=0
maxIndex1=-1
maxIndex2=-1
i=0
while(i<len(song_n_f)-1):
    if(song_n_f[i]>max1):
        max2=max1
        maxIndex2=maxIndex1
        max1=song_n_f[i]
        maxIndex1=i
    elif(song_n_f[i]>max2):
        max2=song_n_f[i]
        maxIndex2=i
    i=i+1
Filter = (np.sin(2*np.pi*int(F[maxIndex1])*time) + np.sin(2*np.pi*int(F[maxIndex2])*time))
songFiltered = song_n - Filter
sd.play(songFiltered , 4*1024)
#convert filtered song to frequency domain
songFiltered_f=fft(songFiltered)
songFiltered_f=2/N*np.abs(songFiltered_f[0:np.int(N/2)])
#plot time
plt.figure()
plt.subplot(3,1,1)
plt.plot(time,song)
plt.subplot(3,1,2)
plt.plot(time,song_n)
plt.subplot(3,1,3)
plt.plot(time,songFiltered)
#plot frequency
plt.figure()
plt.subplot(3,1,1)
plt.plot(F,song_f)
plt.subplot(3,1,2)
plt.plot(F,song_n_f)
plt.subplot(3,1,3)
plt.plot(F,songFiltered_f)
'end'


# #C4=261.63
# #D4=293.66974569918125
# #E4=329.63314428399565
# # F4=349.2341510465061
# # G4=392.0020805232462
# # A4=440.00745824565865
# # B4=493.89167285382297





# # note1 = np.reshape( np.sin (2 * np.pi * C4 * time)*[(time)>=0]*[(time)<=0.3],np.shape(time))
# # note2 = np.reshape( np.sin (2 * np.pi * C4 * time)*[(time)>=0.4]*[(time)<=0.7],np.shape(time))
# # note3 = np.reshape( np.sin (2 * np.pi * G4 * time)*[(time)>=0.8]*[(time)<=1.1],np.shape(time))
# # note4 = np.reshape( np.sin (2 * np.pi * G4 * time)*[(time)>=1.2]*[(time)<=1.5],np.shape(time))
# # note5 = np.reshape( np.sin (2 * np.pi * A4 * time)*[(time)>=1.6]*[(time)<=1.9],np.shape(time))
# # note6 = np.reshape( np.sin (2 * np.pi * A4 * time)*[(time)>=2.0]*[(time)<=2.3],np.shape(time))
# # note7 = np.reshape( np.sin (2 * np.pi * G4 * time)*[(time)>=2.4]*[(time)<=2.7],np.shape(time))
# # note8 = np.reshape( np.sin (2 * np.pi * F4 * time)*[(time)>=3.2]*[(time)<=3.5],np.shape(time))
# # note9 = np.reshape( np.sin (2 * np.pi * F4 * time)*[(time)>=3.6]*[(time)<=3.9],np.shape(time))
# # note10 = np.reshape( np.sin (2 * np.pi * E4 * time)*[(time)>=4.0]*[(time)<=4.3],np.shape(time))
# # note11 = np.reshape( np.sin (2 * np.pi * E4 * time)*[(time)>=4.4]*[(time)<=4.7],np.shape(time))
# # note12 = np.reshape( np.sin (2 * np.pi * D4 * time)*[(time)>=4.8]*[(time)<=5.1],np.shape(time))
# # note13 = np.reshape( np.sin (2 * np.pi * D4 * time)*[(time)>=5.2]*[(time)<=5.5],np.shape(time))
# # note14 = np.reshape( np.sin (2 * np.pi * C4 * time)*[(time)>=5.6]*[(time)<=5.9],np.shape(time))



