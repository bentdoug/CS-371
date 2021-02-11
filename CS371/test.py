import numpy as np
import matplotlib.pyplot as plt

pix = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(pix, pix)
I = np.exp(-(X**2 + Y**2))
plt.imshow(I)
plt.show()
