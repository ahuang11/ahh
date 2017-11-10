import numpy as np
import numpy.ma as ma

x = np.array([1, 2, 3, np.nan, 5])

m = np.ma.array(x, mask=(~np.isfinite(x) | (x == -999)))

print(np.max(m))
print(np.ma.max(m))