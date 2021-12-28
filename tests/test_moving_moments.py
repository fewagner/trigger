
import numpy as np
import trigger as tr

if __name__ == '__main__':
    x = np.random.normal(size=10)
    x[5] = -100

    print('init: ', np.mean(x[:2]), np.var(x[:2]))

    for i in range(2, 10):
        print('---')
        print('true add: ', np.mean(x[i - 2:i + 1]), tr.var(x[i - 2:i + 1]))
        print('function add', tr.add_to_moments(x[i], np.mean(x[i - 2:i]), tr.var(x[i - 2:i]), 2))
        print('true sub: ', np.mean(x[i - 1:i + 1]), tr.var(x[i - 1:i + 1]))
        print('function sub', tr.sub_from_moments(x[i - 2], np.mean(x[i - 2:i + 1]), tr.var(x[i - 2:i + 1]), 3))