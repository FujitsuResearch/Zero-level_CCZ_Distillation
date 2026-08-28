import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit 
import scienceplots
from math import comb, ceil
    
plt.style.use(['science','ieee'])
# plt.xlim(0, 300)
# plt.ylim(1e-7,1e-2)
plt.xlim(10, 1000)
plt.ylim(1e-5,1e-2)
plt.xscale('log')
plt.yscale('log')
# plt.xticks(range(0, 18, 3))
plt.grid()
plt.xlabel("Spacetime Overhead / Success Rate")
plt.ylabel("Logical Error Rate")

ler_t = 1.04e-4
ler_clt = [
    0.006149364854867,
    0.002697954400974,
    0.001193576405196,
    0.000426133930864,
    0.0001887914295208,
    0.00008542056869579,
    0.00002251602171463,
    0.000005870370429897,
    0.000003629267071665,
    0.000002652826930676,
]

ler_ccz = 0.00034852566383247535
ler_8t = 2.8e-5
ler_7t = 1 - (1 - ler_t) ** 7
ler_4t = 1 - (1 - ler_t) ** 4
ler_clt_4t = [1 - (1 - ler) ** 4 for ler in ler_clt]
ler_clt_7t = [1 - (1 - ler) ** 7 for ler in ler_clt]
# print(ler_clt_4t)

suc_ccz = 0.275446
suc_t = 0.6639318
suc_7t = (2 * suc_t - suc_t**2) ** 3 * suc_t**4
suc_4t = suc_t ** 4
suc_8t = (1 - 0.001) ** 8
# print(suc_ccz, suc_4t, suc_7t, suc_8t)
suc_clt = [
    0.735250353832,
    0.731556788408,
    0.726459878104,
    0.710557012833,
    0.688566866858,
    0.654061304043,
    0.556302084452,
    0.488676548255,
    0.418909833541,
    0.307642660846,
]

overhead_ccz_para = 9 / suc_ccz
overhead_t_para_4 = (7 * 16) / suc_4t
overhead_t_para_8 = 135 / suc_8t
overhead_t_para_7 = 44 / suc_7t
# print(overhead_ccz_para, overhead_t_para_4, overhead_t_para_7, overhead_t_para_8)
sp_overhead_clt_4 = 7 * 16
sp_overhead_clt_7 = 44
overhead_clt_4 = [sp_overhead_clt_4 / (suc ** 4) for suc in suc_clt]
# print(overhead_clt_4)
overhead_clt_7 = [sp_overhead_clt_7 / ((2 * suc - suc**2) ** 3 * suc**4) for suc in suc_clt]
# print(overhead_clt_7)

plt.scatter(overhead_ccz_para, ler_ccz, marker = "o", s = 8, c = "b", label = "Zero-level CCZ")
plt.scatter(overhead_t_para_4, ler_4t, marker = "^", s = 8, c = "orange", label = "Zero-level $\\times$ 4")
plt.scatter(overhead_t_para_7, ler_7t, marker = "^", s = 8, c = "orangered", label = "Zero-level $\\times$ 7")
plt.scatter(overhead_clt_4, ler_clt_4t, marker = ",", s = 8, c = "purple", label = "Cultivation $\\times$ 4")
plt.scatter(overhead_clt_7, ler_clt_7t, marker = ",", s = 8, c = "brown", label = "Cultivation $\\times$ 7")
plt.scatter(overhead_t_para_8, ler_8t, marker = "x", s = 8, c = "green", label = "$T \\times 8$ Distillation")

plt.legend(fontsize="xx-small", loc="upper left")

plt.savefig("overhead_LER.pdf")
