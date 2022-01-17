import trigger as tr
import pickle
import numpy as np

header, keys, adc_bits, dac_bits, dt_tcp = tr.read_header('../../COSINUS_DATA/data_newOP_ncal_57Co_002.bin')

print(header)

data = np.fromfile('../../COSINUS_DATA/data_newOP_ncal_57Co_002.bin',
                   dtype=dt_tcp,
                   count=100,
                   offset=header.nbytes)

print(data['Time'] - data['Time'][0])