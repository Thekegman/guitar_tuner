import numpy as np
from scipy.io import wavfile
import sounddevice as sd
from scipy.signal import find_peaks

from matplotlib.pyplot import show, plot
fs = 8000
data = sd.rec(int(0.5 * fs), samplerate=fs, channels=1)
sd.wait()
audio = data[900*2:900*2+80*2,0]

plot(data)
show()
#audio = np.array([np.sin(2*np.pi*1000*n/44100) for n in range(44100*1)])


corr = np.correlate(audio,audio, 'full')[audio.size-1:]
corr = corr*[1+0.008*i for i in range(corr.size)]
peaks,dics = find_peaks(corr, height = 0)
top = np.argsort(corr[peaks])[-2:]
ind = top[-1]
print("diff" ,np.diff(corr[peaks[top]]))
#if np.diff(corr[peaks[top]])[-1] <1E-7:
#    ind = top[-2]
print(peaks[ind]) 
print(fs/peaks[ind], "hz")
plot(corr)
plot(peaks[top], corr[peaks[top]], "x")
show()
#sd.play(audio)

#sd.wait()
#maybe check to see by how much a peak is the largest
#np.correlate()
