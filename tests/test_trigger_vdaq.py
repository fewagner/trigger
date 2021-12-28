import pyfftw
import trigger as tr
import numpy as np
from scipy.signal import firwin
import matplotlib.pyplot as plt
import pickle

if __name__ == '__main__':
    trigger = tr.VTrigger('../../COSINUS_DATA/data_newOP_ncal_57Co_002.bin')
    # filt = firwin(16384, 0.01)
    # filters = np.tile(filt, (2, 1))
    trigger.setup(batchsize=1048576, threshold=5, lag=512, look_ahead=512,  # adc_filters=filters,
                  adc_channels=[1, 2], dac_channels=[1, 3],
                  adc_fixed_var=[0.000064, 0.000064],
                  dac_fixed_var=[0.003, 0.000064])
    triggers_dac, triggers_adc = trigger.go()

    with open('vdaqtriggers', 'wb') as f:
        pickle.dump([triggers_dac, triggers_adc], f)

    with open('vdaqtriggers', 'rb') as f:
        triggers_dac, triggers_adc = pickle.load(f)

    plt.scatter(triggers_adc[0][2], triggers_adc[0][1], rasterized=True, marker='o', s=10)
    plt.title('PH-Offset ADC1')
    plt.show()

    plt.scatter(triggers_adc[1][2], triggers_adc[1][1], rasterized=True, marker='o', s=10)
    plt.title('PH-Offset ADC2')
    plt.show()

    plt.scatter(triggers_adc[0][0], triggers_adc[0][2], rasterized=True, marker='o', s=10)
    plt.title('Offset ADC1')
    plt.show()

    plt.scatter(triggers_adc[1][0], triggers_adc[1][2], rasterized=True, marker='o', s=10)
    plt.title('Offset ADC2')
    plt.show()

    x = np.diff(triggers_adc[0][0])
    print(np.mean(x[x > 1024]))
    plt.hist(x[x > 1024], bins=100, range=(0, 50000))
    plt.title('Waiting Time ADC1')
    plt.show()

    x = np.diff(triggers_adc[1][0])
    print(np.mean(x[x > 1024]))
    plt.hist(x[x > 1024], bins=100, range=(0, 50000))
    plt.title('Waiting Time ADC2')
    plt.show()

    plt.hist(triggers_adc[0][1], bins=100, range=(0, 1))
    # plt.yscale('log')
    plt.title('Pulse heights ADC1')
    plt.show()

    plt.hist(triggers_adc[1][1], bins=100, range=(0, 1))
    # plt.yscale('log')
    plt.title('Pulse heights ADC2')
    plt.show()

    plt.hist(triggers_dac[0][1], bins=100)
    # plt.yscale('log')
    plt.title('Pulse heights DAC1')
    plt.show()

    plt.hist(triggers_dac[1][1], bins=100)
    # plt.yscale('log')
    plt.title('Pulse heights DAC3')
    plt.show()
