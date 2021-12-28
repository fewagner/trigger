from trigger import get_triggers, var, oaconvolve
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin
from scipy.signal import oaconvolve
import pyfftw

if __name__ == '__main__':

    # create mock data
    duration = 10  # in sec
    sample_frequency = 25000  # in Hz
    rate = 1  # in Hz
    pulse_decay = 1  # in sec
    amplitude = 1
    resolution = 0.1
    x = np.arange(0, duration, 1 / sample_frequency)  # in sec
    y = np.random.normal(loc=0, scale=resolution, size=x.shape[0])  # in V
    hits = []
    hit = duration + 1
    while hit > duration:  # make sure there is at leadt one hit
        hit = np.random.exponential(scale=1 / rate)  # in sec
    while hit < duration:
        hits.append(hit)
        y[int(hit * sample_frequency):] += amplitude*np.exp(-x[:-int(hit * sample_frequency)] / pulse_decay)
        hit += np.random.exponential(scale=1 / rate)

    # create a low pass filter
    filter = firwin(10000, 0.01)

    # create the filter
    matched_filter = np.flip(np.exp(-x[:10000] / pulse_decay))/np.sum(np.exp(-x[:10000] / pulse_decay))

    # plot the filters
    plt.close()
    plt.loglog(np.fft.rfftfreq(10000, 1/sample_frequency),
               np.abs(np.fft.rfft(filter))**2, label='low pass')
    plt.loglog(np.fft.rfftfreq(10000, 1/sample_frequency),
               np.abs(np.fft.rfft(matched_filter))**2, label='matched_filter')
    plt.ylabel('Filter amplification')
    plt.xlabel('Frequency (Hz)')
    plt.show()

    # filter the data with scipy
    y_filtered = oaconvolve(y, filter, mode='same')
    y_matched_filtered = oaconvolve(y, matched_filter, mode='same')
    print(y_filtered.shape)
    print(y_matched_filtered.shape)

    y_filtered = oaconvolve(y, filter, mode='full')
    y_matched_filtered = oaconvolve(y, matched_filter, mode='full')
    print(y_filtered.shape)
    print(y_matched_filtered.shape)

    y_filtered = oaconvolve(y, filter, mode='valid')
    y_matched_filtered = oaconvolve(y, matched_filter, mode='valid')
    print(y_filtered.shape)
    print(y_matched_filtered.shape)

    # plot

    plt.close()
    plt.plot(x, y, linewidth=0.1, color='C0', label='measured')
    plt.plot(x, y_filtered, linewidth=1, color='C1', label='low pass')
    plt.plot(x, y_matched_filtered, linewidth=2, color='red', label='matched filter')
    for h in hits:
        plt.axvline(x=h, color='grey', alpha=0.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (V)')
    plt.tight_layout()
    plt.show()
