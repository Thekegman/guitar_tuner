import numpy as np
import shutil
import sounddevice as sd
from scipy.signal import find_peaks
from matplotlib.pyplot import show, plot
fs = 44100
block_size = fs//40
ignore_count = fs//4
frame_count = 0
guitar_frequency_map = {82 : "E", 110 : "A", 147 : "D", 196 : "G", 247 : "B", 330 : "E"}

def get_prompt(freq1 , freq2):
    closest_target_f1 = min(guitar_frequency_map, key=lambda x:abs(x-freq1))
    closest_target_f2 = min(guitar_frequency_map, key=lambda x:abs(x-freq2))
    if abs(freq1 -82*2) < 7 and abs(freq2*2 -freq1) < 6:
        closest_target_f = closest_target_f2
        freq = freq2
    else:
        #print(abs(freq1 -82*2), abs(freq2*2 -freq1))
        closest_target_f = closest_target_f1
        freq = freq1
        
    diff = freq-closest_target_f
    if diff < 90:
        if abs(diff) < 1.5:
            print(guitar_frequency_map[closest_target_f],"In Tune!", end="        \r")
        elif diff > 0:
            print(guitar_frequency_map[closest_target_f], "String Too High", end="        \r")
        else:
            print(guitar_frequency_map[closest_target_f], "String Too Low", end="        \r")
        return True
    else:
        return False

def callback(indata, frames, time, status):
    global frame_count
    frame_count+=indata.size
    if frame_count > ignore_count:
        audio = indata[:,0]
        corr = np.correlate(audio,audio, 'full')[audio.size-1:]
       # corr = corr*[1+0.007*i for i in range(corr.size)]
        peaks,dics = find_peaks(corr, height = 0)
        if peaks.size >0:
            top = np.argsort(corr[peaks])[-2:]
            ind = top[-1]
                
            power = corr[0]/audio.size
            if power>5E-7 and corr[peaks[ind]]> corr[0]*0.01:
               # print(fs/peaks[top])
                get_prompt(fs/peaks[top[-1]], fs/peaks[top[-2]])
            else:
                print("", end="                  \r")



with sd.InputStream(channels=1,samplerate=fs, blocksize=block_size, callback=callback):
    input()

