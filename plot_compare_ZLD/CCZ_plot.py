import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit 
import scienceplots
from math import comb
    

from math import comb

def prob_at_least_four(k: int, p: float) -> float:
    # return sum(comb(k, i) * (p ** i) * ((1 - p) ** (k - i)) for i in range(4, k + 1))
    return sum(comb(k, i) * (p ** i) * ((1 - p) ** (k - i)) for i in range(7, k + 1))

prob_list = [1e-3, 8e-4, 6e-4, 4e-4, 2e-4, 1e-4]
logical_error_rate_ungrown = [0.0002703683888719046, 0.00019523066744384006, 0.00010763579824934929, 4.65009456137416e-05, 1.1667975146736694e-05, 3.1638657726672983e-06]
success_rate_ungrown = [0.418688, 0.4978726, 0.5927396, 0.705362, 0.8399058, 0.9166002]
logical_error_rate_grown = [0.00034852566383247535, 0.0002219381364258208, 0.00011960131162771752, 5.422499759000011e-05, 1.3586052894515038e-05, 3.866977783985162e-06]
success_rate_grown = [0.275446, 0.3568562, 0.4615334, 0.5975104, 0.7728514, 0.8792396]

prob_7c = [1e-3, 7e-4, 5e-4, 3e-4, 1e-4]
error_7c = [1.04e-04, 5.67e-05, 3.07e-05, 1.02e-05, 1.82e-06]
suc_7c = [0.6639318, 0.7417831, 0.8076152, 0.8797074, 0.9581302]

suc_ccz = success_rate_grown[0]
suc_t = suc_7c[0]


# suc_ccz_para_x = list(range(3, 12, 3))
# suc_ccz_para_y = [1 - (1 - suc_ccz) ** k for k in range(1, 4)]
suc_ccz_para_x = list(range(3, 18, 3))
suc_ccz_para_y = [1 - (1 - suc_ccz) ** k for k in range(1, 6)]
# suc_t_para_x = list(range(4, 16))
# suc_t_para_y = [prob_at_least_four(k, suc_t) for k in range(4, 16)]
suc_t_para_x = list(range(7, 16))
suc_t_para_y = [prob_at_least_four(k, suc_t) for k in range(7, 16)]


plt.style.use(['science','ieee'])

plt.scatter(suc_ccz_para_x, suc_ccz_para_y, marker = "x", s = 10, c = "b", label = "Grown")
plt.scatter(suc_t_para_x, suc_t_para_y, marker = ",", s = 5, c = "orange", label = "Zero-level $\\times$ 7")

plt.xlim(0, 15)
plt.ylim(0, 1)
plt.xticks(range(0, 18, 3))
plt.grid(alpha=0.5)
plt.xlabel("Number of Logical Qubits")
plt.ylabel("Success Rate")
plt.legend(fontsize="x-small", loc="upper left")

plt.savefig("Success_rate_para.png", dpi = 500)