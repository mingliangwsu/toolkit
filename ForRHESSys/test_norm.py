from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-1, 1, 100)

mean = 0
std = 0.5

plt.plot(x, norm.pdf(x, loc=mean, scale=std))
plt.show()