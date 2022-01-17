import cait as ai
import trigger as tr
import matplotlib.pyplot as plt
import pickle
import numpy as np
import sys

header, keys, adc_bits, dac_bits, dt_tcp = tr.read_header('../../COSINUS_DATA/data_newOP_ncal_57Co_002.bin')

key = 'DAC1'
longer = 1
bits = adc_bits if 'ADC' in key else dac_bits

with open('vdaqtriggers', 'rb') as f:
    triggers_dac, triggers_adc = pickle.load(f)

for idx in range(1000, 1010):
    trigger_time = triggers_dac[0][0][idx]*0.00001
    start_time = trigger_time - 16384/4*0.00001
    threshold = 5*np.sqrt(triggers_dac[0][3][idx]) + triggers_dac[0][2][idx]
    height = triggers_dac[0][1][idx] + triggers_dac[0][2][idx]
    # sys.exit()

    print('###')
    print(start_time)
    print(height)
    print(threshold)

    event, time = ai.trigger.get_record_window_vdaq(path='../../COSINUS_DATA/data_newOP_ncal_57Co_002.bin',
                                                    start_time=start_time,
                                                    record_length=16384*longer,
                                                    dtype=dt_tcp,
                                                    key=key,
                                                    header_size=header.itemsize,
                                                    sample_duration=0.00001,
                                                    down=longer,
                                                    bits=bits)
    if 'DAC' in key:
        event **= 2

    plt.plot(time, event)
    plt.axvline(x=trigger_time, color='grey', linestyle='dashed', linewidth=2)
    plt.axhline(y=height, color='grey', linestyle='dashed', linewidth=2)
    plt.axhline(y=threshold, color='black', linewidth=0.5)
    plt.show()
