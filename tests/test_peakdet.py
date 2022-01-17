import cait as ai

args = {'adc_channels': [1, 2],
        'dac_channels': [1, 3],
        'record_length': 8192,
        'sample_frequency': 100000,
        'path_h5': '../../COSINUS_DATA/',
        'fname': 'data_newOP_ncal_57Co_002',
        'path_bin': '../../COSINUS_DATA/data_newOP_ncal_57Co_002.bin',
        }

dh = ai.DataHandler(channels=args['adc_channels'],
                    record_length=args['record_length'],
                    sample_frequency=args['sample_frequency'])

dh.set_filepath(path_h5=args['path_h5'],
                fname=args['fname'],
                appendix=False)

dh.calc_peakdet()