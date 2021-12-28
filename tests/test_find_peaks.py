from trigger import find_peaks, var
import numpy as np
import matplotlib.pyplot as plt

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

    # trigger the data
    lag = 300
    threshold = 5
    signal, all_means, all_vars = find_peaks(array=y,
                                             lag=lag,
                                             threshold=threshold,
                                             init_mean=np.mean(y[:lag]),
                                             init_var=var(y[:lag]))

    # plot

    fig, axes = plt.subplots(2, 1)
    axes[0].plot(x, y, linewidth=0.1)
    axes[0].plot(x, all_means, color='black')
    for h in hits:
        axes[0].axvline(x=h, color='red', alpha=0.5)
    axes[1].fill_between(x, (y - all_means) + threshold * np.sqrt(all_vars),
                         (y - all_means) - threshold * np.sqrt(all_vars),
                         color='yellow')
    axes[1].plot(x, y - all_means, color='black', linewidth=0.3)
    axes[1].plot(x, signal, color='red')
    fig.supxlabel('Time (s)')
    fig.supylabel('Amplitude (V)')
    plt.tight_layout()
    plt.show()
