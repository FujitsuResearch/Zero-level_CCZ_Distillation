import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit 
import scienceplots
from math import comb, ceil
    
plt.style.use(['science','ieee'])
plt.xlim(0, 200)
plt.ylim(0, 1)
# plt.xticks(range(0, 18, 3))
plt.grid()
plt.xlabel("Spacetime Overhead")
plt.ylabel("Success Rate")


def prob_at_least_four(k: int, p: float) -> float:
    # return sum(comb(k, i) * (p ** i) * ((1 - p) ** (k - i)) for i in range(4, k + 1))
    return sum(comb(k, i) * (p ** i) * ((1 - p) ** (k - i)) for i in range(7, k + 1))

suc_ccz = 0.275446
suc_t = 0.6639318

# k = list(range(1, 10))
k2 = list(range(2, 10))

suc_ccz_para_x = [i * 9 for i in range(1, 20)]
suc_ccz_para_y = [1 - (1 - suc_ccz) ** k for k in range(1, 20)]
suc_t_para_x_4 = [16 * i + 16 * ceil(i / 2) + 80 for i in range(1, 10)]
suc_t_para_y_4 = [(1 - (1 - suc_t) ** k) ** 4 for k in range(1, 10)]
suc_t_para_x_8 = [135 * i for i in range(1, 10)]
suc_t_para_y_8 = [1 - (1 - (1 - 0.001) ** 8) ** k for k in range(1, 10)]
suc_t_para_x_7 = [22 * i for i in k2]
suc_t_para_y_7 = [((1 - (1 - suc_t) ** k) ** 3) * ((1 - (1 - suc_t)**k - k * suc_t * (1 - suc_t)**(k - 1)) ** 2) for k in range(2, 10)]



plt.scatter(suc_ccz_para_x, suc_ccz_para_y, marker = "x", s = 10, c = "b", label = "Zero-level_CCZ")
plt.scatter(suc_t_para_x_4, suc_t_para_y_4, marker = "^", s = 5, c = "orange", label = "Zero-level $\\times$ 4")
plt.scatter(suc_t_para_x_7, suc_t_para_y_7, marker = "v", s = 5, c = "orangered", label = "Zero-level $\\times$ 7")
plt.scatter(suc_t_para_x_8, suc_t_para_y_8, marker = ",", s = 5, c = "green", label = "$T \\times 8$ Distillation")

plt.legend(fontsize="x-small", loc="lower right")

plt.savefig("Success_rate_para.pdf")