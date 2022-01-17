import cait as ai
import pickle
import numpy as np
import trigger as tr

# args

args = {'adc_channels': [1, 2],
        'dac_channels': [1, 3],
        'record_length': 8192,
        'sample_frequency': 100000,
        'path_h5': '../../COSINUS_DATA/',
        'fname': 'data_newOP_ncal_57Co_002',
        'path_bin': '../../COSINUS_DATA/data_newOP_ncal_57Co_002.bin',
        }

# read header

header, keys, adc_bits, dac_bits, dt_tcp = tr.read_header(args['path_bin'])

print(adc_bits, dac_bits)

# get triggers from pickle file

with open('vdaqtriggers', 'rb') as f:
    triggers_dac, triggers_adc = pickle.load(f)

# init empty hdf5

dh = ai.DataHandler(channels=args['adc_channels'],
                    record_length=args['record_length'],
                    sample_frequency=args['sample_frequency'])

dh.set_filepath(path_h5=args['path_h5'],
                fname=args['fname'],
                appendix=False)

dh.init_empty()

# include the triggers to hdf5

dh.include_vtrigger_stamps(triggers=[triggers_adc[0][0] / args['sample_frequency'],
                                     triggers_adc[1][0] / args['sample_frequency']],
                           name_appendix='',
                           trigger_block=args['record_length'],
                           file_start=triggers_adc[0][4][0] / 1e9)

# inlcude the test stamps

dh.include_test_stamps_vdaq(triggers=[triggers_dac[0][0] / args['sample_frequency'],
                                      triggers_dac[1][0] / args['sample_frequency']],
                            tpas=[triggers_dac[0][1],
                                  triggers_dac[1][1]],
                            name_appendix='',
                            trigger_block=args['record_length'],
                            file_start=triggers_adc[0][4][0] / 1e9)

# include triggered events and test pulses

dh.include_triggered_events_vdaq(path=args['path_bin'],
                                 dtype=dt_tcp,
                                 keys=['ADC' + str(i) for i in args['adc_channels']],
                                 header_size=header.itemsize,
                                 adc_bits=adc_bits,
                                 max_time_diff=3 / 4 * args['record_length'] / args['sample_frequency'],  # in sec
                                 exclude_tp=True,
                                 min_tpa=[0.001, 0.001],
                                 min_cpa=[100.1, 100.1],
                                 )

# include noise triggers

dh.include_noise_triggers(nmbr=5000,
                          min_distance=3 / 4 * args['record_length'] / args['sample_frequency'],
                          max_distance=60,
                          max_attempts=5,
                          )

# include noise events

dh.include_noise_events_vdaq(path=args['path_bin'],
                             dtype=dt_tcp,
                             keys=['ADC' + str(i) for i in args['adc_channels']],
                             header_size=header.itemsize,
                             adc_bits=adc_bits,
                             )
