import trigger as tr
import numpy as np
from scipy.signal import oaconvolve, convolve
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = np.random.normal(loc=2, size=16)
    y = np.array([1, 1, 1, 1])/4
    x_ = oaconvolve(x, y)
    x___ = oaconvolve(x, y, mode='same')
    x1_ = oaconvolve(x[:8], y)
    x2_ = oaconvolve(x[8:], y)
    x__ = np.zeros(x_.shape)
    x__[:x1_.shape[0]] += x1_
    x__[-x2_.shape[0]:] += x2_

    print(x_)
    print(x__)

    plt.plot(np.arange(16), x, label='original')
    plt.plot(np.arange(16), x___, label='filtered same')
    plt.plot(np.arange(-1, 18), x_, label='filtered full')
    plt.plot(np.arange(-1, 10), x1_, label='first half')
    plt.plot(np.arange(7, 18), x2_, label='second half')
    plt.plot(np.arange(-1, 18), x__, label='added full', linestyle='dashed')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()
