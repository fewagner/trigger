"""
Extension for VDAQ data formats.
"""
import numpy as np
import numba as nb
from scipy.signal import oaconvolve
import os
from tqdm.auto import trange
from ._core import get_triggers, var

def bin(s, nmbr_bits=None):
    """
    Returns a string of 0/1 values for any datatype
    :param s: any
    :return: string, the 0/1's of s' bits
    """
    bit_list = str(s) if s <= 1 else bin(s >> 1) + str(s & 1)
    if nmbr_bits is not None:
        while len(bit_list) < nmbr_bits:
            bit_list = '0' + bit_list
    return bit_list

@nb.njit
def volt(x, uswing=39.3216, bits=16):
    """
    Calculates the volt value from a given integer from an ADC
    :param x: int, the integer that is to covnert to volt
    :param uswing: float, the maximal range of the ADC
    :param bits: int, the sampling resolution
    :return: float, the converted volt value
    """
    return x * (uswing / (2 ** bits - 1))


def read_header(path_bin):
    """
    Function that reads the header of a *.bin file
    :param f: filestream, the stream of the *.bin file
    :return: tuple (dictionary with infos from header,
                    list of keys that are written in each sample,
                    bool True if adc is 16 bit,
                    bool True if dac is 16 bit)
    """

    keys = []

    dt_header = np.dtype([('ID', 'i4'),
                          ('numOfBytes', 'i4'),
                          ('downsamplingFactor', 'i4'),
                          ('channelsAndFormat', 'i4'),
                          ('timestamp_low', 'i4'),
                          ('timestamp_high', 'i4'),
                          ])

    header = np.fromfile(path_bin, dtype=dt_header, count=1)[0]

    channelsAndFormat = bin(header['channelsAndFormat'], 32)

    # print('channelsAndFormat: ', channelsAndFormat)

    # bit 0: Timestamp uint64
    if channelsAndFormat[-1] == '1':
        keys.append('TimeLow')
        keys.append('TimeHigh')

    # bit 1: settings uint32
    if channelsAndFormat[-2] == '1':
        keys.append('Settings')

    # bit 2-5: dac 1-4
    for c, b in enumerate([2, 3, 4, 5]):
        if channelsAndFormat[-int(b + 1)] == '1':
            keys.append('DAC' + str(c + 1))

    # bit 6-8: adc 1-3
    for c, b in enumerate([6, 7, 8]):
        if channelsAndFormat[-int(b + 1)] == '1':
            keys.append('ADC' + str(c + 1))

    # bit 9-16: -

    # bit 16: 0...DAC 16 bit, 1...DAC 32 bit
    if channelsAndFormat[-17] == '1':
        dac_short = False
    else:
        dac_short = True

    # bit 17: 0...ADC 16 bit, 1...ADC 32 bit
    if channelsAndFormat[-18] == '1':
        adc_short = False
    else:
        adc_short = True

    # bit 18-31: -

    # construct data type

    dt_tcp = []

    for k in keys:
        if k.startswith('Time') or k.startswith('Settings'):
            dt_tcp.append((k, 'i4'))
        elif k.startswith('DAC'):
            if dac_short:
                dt_tcp.append((k, 'i2'))
            else:
                dt_tcp.append((k, 'i4'))
        elif k.startswith('ADC'):
            if adc_short:
                dt_tcp.append((k, 'i2'))
            else:
                dt_tcp.append((k, 'i4'))

    dt_tcp = np.dtype(dt_tcp)

    if adc_short:
        adc_bits = 16
    else:
        adc_bits = 24
    if dac_short:
        dac_bits = 16
    else:
        dac_bits = 24

    return header, keys, adc_bits, dac_bits, dt_tcp


class VTrigger():

    def __init__(self, path):
        self.path = path

    def setup(self, batchsize=1048576, samples=None, threshold=5, lag=512, look_ahead=512,
              adc_filters=None, dac_channels=None, adc_channels=None):
        self.header, self.keys, self.adc_bits, self.dac_bits, self.dt_tcp = read_header(self.path)
        if samples is None:
            self.samples = int((os.path.getsize(self.path) - self.header.nbytes)/self.dt_tcp.itemsize)
        else:
            self.samples = samples
        self.nmbr_batches = int(self.samples/batchsize)
        self.batchsize = batchsize
        self.threshold=threshold
        self.lag=lag
        self.look_ahead=look_ahead

        if dac_channels is None:
            self.dac_channels = [0, 1, 2, 3]
        else:
            self.dac_channels = dac_channels
        self.dac_channels = ['DAC' + str(i) for i in self.dac_channels if 'DAC' + str(i) in self.keys]

        if adc_channels is None:
            self.adc_channels = [0, 1]
        else:
            self.adc_channels = adc_channels
        self.adc_channels = ['ADC' + str(i) for i in self.adc_channels if 'ADC' + str(i) in self.keys]

        if adc_filters is not None:
            self.adc_filters = adc_filters
        else:
            self.adc_filters = [None for i in self.adc_channels]

    def go(self):
        triggers_dac = []
        for k in self.dac_channels:
            triggers_dac.append(self.trigger(k, None, self.dac_bits))

        triggers_adc = []
        for i, k in enumerate(self.adc_channels):
            triggers_adc.append(self.trigger(k, self.adc_filters[i], self.adc_bits))

        return triggers_dac, triggers_adc

    def trigger(self, key, filter, bits):
        mean, variance = None, None
        signal, heights, all_means, all_vars = [], [], [], []
        if filter is not None:
            filter_length = filter.shape[0]
            overlap = np.zeros(filter_length - 1)
        for b in trange(self.nmbr_batches):
            data = np.fromfile(self.path, dtype=self.dt_tcp, count=self.batchsize,
                               offset=self.header.nbytes + b * self.batchsize * self.dt_tcp.itemsize)

            stream = volt(data[key], bits=bits)
            if filter is not None:
                stream = oaconvolve(stream, filter, mode='full')
                stream[:filter_length - 1] += overlap
                overlap = stream[-int(filter_length - 1):]
                stream = stream[:-int(filter_length - 1)]

            if mean is None:
                mean = np.mean(stream[:self.lag])
            if variance is None:
                variance = var(stream[:self.lag])

            signal_, heights_, all_means_, all_vars_ = get_triggers(stream, self.lag, self.threshold,
                                                                mean, variance, self.look_ahead)
            mean, variance = np.mean(stream[-self.lag:]), var(stream[-self.lag:])
            signal.extend(signal_)
            heights.extend(heights_)
            all_means.extend(all_means_)
            all_vars.extend(all_vars_)

        signal = np.array(signal)
        heights = np.array(heights)
        all_means = np.array(all_means)
        all_vars = np.array(all_vars)

        return signal, heights, all_means, all_vars