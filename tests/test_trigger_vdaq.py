import pyfftw
import trigger as tr
import numpy as np
from scipy.signal import firwin
import matplotlib.pyplot as plt
import pickle

if __name__ == '__main__':
    # trigger = tr.VTrigger('../../COSINUS_DATA/data_newOP_ncal_57Co_002.bin')
    # filt = firwin(16384, 0.01)
    # filters = np.tile(filt, (2, 1))
    # trigger.setup(batchsize=1048576, threshold=5, lag=512, look_ahead=512,  # adc_filters=filters,
    #               adc_channels=[1, 2], dac_channels=[1, 3])
    # triggers_dac, triggers_adc = trigger.go()

    # with open('vdaqtriggers', 'wb') as f:
    #     pickle.dump([triggers_dac, triggers_adc], f)

    with open('vdaqtriggers', 'rb') as f:
        triggers_dac, triggers_adc = pickle.load(f)

    print(triggers_adc[0][1].shape)

    plt.hist(triggers_adc[0][1], bins=100, range=(0,1))
    plt.yscale('log')
    plt.title('Pulse heights ADC1')
    plt.show()

    plt.hist(triggers_dac[0][1], bins=100)
    plt.yscale('log')
    plt.title('Pulse heights DAC1')
    plt.show()