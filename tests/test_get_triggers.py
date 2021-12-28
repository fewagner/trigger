from trigger import get_triggers, var
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
    signal, heights, all_means, all_vars = get_triggers(array=y,
                                             lag=lag,
                                             threshold=threshold,
                                             init_mean=np.mean(y[:lag]),
                                             init_var=var(y[:lag]),
                                             look_ahead=100,
                                             fixed_var=0.01)

    print(signal)

    # plot

    plt.plot(x, y, linewidth=0.1)
    for h in hits:
        plt.axvline(x=h, color='grey', alpha=0.5)
    plt.vlines(x=x[signal], ymin=all_means, ymax=np.array(all_means) + np.array(heights) - np.sqrt(all_vars),
               color='red', linewidth=2, zorder=50)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (V)')
    plt.tight_layout()
    plt.show()
