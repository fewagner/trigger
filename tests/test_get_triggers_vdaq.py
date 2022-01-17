from trigger import read_header, volt, get_triggers, var
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin
from scipy.signal import oaconvolve

if __name__ == '__main__':
    # load data
    path = '../../COSINUS_DATA/data_newOP_ncal_57Co_002.bin'
    key = 'ADC1'
    header, keys, adc_bits, dac_bits, dt_tcp = read_header(path)
    batchsize = int(1048576*4/1)
    which_batch = 0
    data = np.fromfile(path,
                       dtype=dt_tcp, count=batchsize,
                       offset=header.nbytes + which_batch * batchsize * dt_tcp.itemsize)

    stream = volt(data[key], bits=adc_bits)

    # create a filter
    import pickle
    with open('sevs', 'rb') as f:
        t, fitted = pickle.load(f)

    filter = np.flip(fitted[0])/np.sum(fitted[0])  # firwin(16384, 0.01)

    stream = oaconvolve(stream, filter, mode='valid')

    # trigger the data

    lag = 1024*4
    sample_frequency = 50000
    signal, heights, all_means, all_vars = get_triggers(array=stream,
                                                        lag=lag,
                                                        threshold=5,
                                                        init_mean=np.mean(stream[:lag]),
                                                        init_var=var(stream[:lag]),
                                                        look_ahead=lag)

    # plot
    x = np.arange(stream.shape[0]) / sample_frequency
    plt.plot(x, stream, linewidth=0.5)
    plt.vlines(x=np.array(signal) / sample_frequency, ymin=all_means,
               ymax=np.array(all_means) + np.array(heights) - np.sqrt(all_vars),
               color='red', linewidth=2, zorder=50)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (V)')
    plt.tight_layout()
    plt.show()
