import numpy as np
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

if __name__ == "__main__":
    # Sampling parameters for 4-channel MEMS geophone array
    fs = 10000.0
    lowcut = 10.0
    highcut = 1000.0
    
    # Simulate raw input signal buffer from I2S ADC
    raw_signal = np.random.normal(0, 1, 1024)
    filtered_signal = bandpass_filter(raw_signal, lowcut, highcut, fs, order=4)
    
    # Compute Fast Fourier Transform for frequency analysis
    fft_result = np.fft.fft(filtered_signal)
    print("DSP Pipeline Executed Successfully. Peak Frequency Bin:", np.argmax(np.abs(fft_result)))