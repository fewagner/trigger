from trigger import find_peaks, var, volt, read_header
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import oaconvolve

if __name__ == '__main__':

    # load data
    path = '../../COSINUS_DATA/data_newOP_ncal_57Co_002.bin'
    key = 'ADC1'
    header, keys, adc_bits, dac_bits, dt_tcp = read_header(path)
    batchsize = int(1048576*2/1)
    which_batch = 0
    data = np.fromfile(path,
                       dtype=dt_tcp, count=batchsize,
                       offset=header.nbytes + which_batch * batchsize * dt_tcp.itemsize)

    stream = volt(data[key], bits=adc_bits)

    # create a filter
    import pickle

    with open('sevs', 'rb') as f:
        t, fitted = pickle.load(f)

    filter = np.flip(fitted[0]) / np.sum(fitted[0])  # firwin(16384, 0.01)

    stream = oaconvolve(stream, filter, mode='valid')
    stream = np.diff(stream)*50000

    # trigger the data

    lag = 1024*8
    threshold = 5
    sample_frequency = 50000
    signal, all_means, all_vars = find_peaks(array=stream,
                                            lag=lag,
                                            threshold=threshold,
                                            init_mean=None,
                                            init_var=None)

    # plot
    x = (which_batch*batchsize + np.arange(0, stream.shape[0])) / sample_frequency

    fig, axes = plt.subplots(2, 1)
    axes[0].plot(x, stream, linewidth=0.5)
    axes[0].plot(x, all_means, color='black')
    axes[1].fill_between(x, (stream - all_means) + threshold * np.sqrt(all_vars),
                         (stream - all_means) - threshold * np.sqrt(all_vars),
                         color='yellow')
    axes[1].plot(x, stream - all_means, color='black', linewidth=0.3)
    axes[1].plot(x, signal, color='red')
    plt.ylim(-3, 3)
    fig.supxlabel('Time (s)')
    fig.supylabel('Amplitude (V)')
    plt.tight_layout()
    plt.show()
