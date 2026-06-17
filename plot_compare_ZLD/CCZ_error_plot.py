import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit 
import scienceplots

prob_list = [1e-3, 8e-4, 6e-4, 4e-4, 2e-4, 1e-4]
logical_error_rate_ungrown = [0.0002703683888719046, 0.00019523066744384006, 0.00010763579824934929, 4.65009456137416e-05, 1.1667975146736694e-05, 3.1638657726672983e-06]
success_rate_ungrown = [0.418688, 0.4978726, 0.5927396, 0.705362, 0.8399058, 0.9166002]
logical_error_rate_grown = [0.00034852566383247535, 0.0002219381364258208, 0.00011960131162771752, 5.422499759000011e-05, 1.3586052894515038e-05, 3.866977783985162e-06]
success_rate_grown = [0.275446, 0.3568562, 0.4615334, 0.5975104, 0.7728514, 0.8792396]

prob_7c = [1e-3, 7e-4, 5e-4, 3e-4, 1e-4]
error_7c = [1.04e-04, 5.67e-05, 3.07e-05, 1.02e-05, 1.82e-06]
suc_7c = [0.6639318, 0.7417831, 0.8076152, 0.8797074, 0.9581302]

def fit_func(x,a):
    return a * x**2

error_7c_4 = []
error_7c_7 = []
for i in range(5):
    error_7c_4.append(1 - (1 - error_7c[i]) ** 4)
    error_7c_7.append(1 - (1 - error_7c[i]) ** 7)

popt2, pcov2 = curve_fit(fit_func, prob_list, logical_error_rate_grown)
print(popt2)
popt_7c_4, pcov_7c = curve_fit(fit_func, prob_7c, error_7c_4)
print(popt_7c_4)
popt_7c_7, pcov_7c = curve_fit(fit_func, prob_7c, error_7c_7)
print(popt_7c_7)


plt.style.use(['science','ieee'])
plt.xscale('log')
plt.yscale('log')
x = np.linspace(1e-4,1e-2,2000)

# plt.scatter(prob_list, logical_error_rate_ungrown, marker = ".", s = 10, c = "r", label = "Ungrown")
# plt.plot(x,fit_func(x, popt[0]),c = "r", label = "Ungrown")
plt.scatter(prob_list, logical_error_rate_grown, marker = "x", s = 10, c = "b", label = "Zero-level_CCZ")
plt.plot(x,fit_func(x, popt2[0]),c = "b", label = "Zero-level_CCZ")
plt.scatter(prob_7c, error_7c_4, marker = "^", s = 5, c = "orange", label = "Zero-level $\\times$ 4")
plt.plot(x,fit_func(x, popt_7c_4[0]), c = "orange", label = "Zero-level $\\times$ 4")
plt.scatter(prob_7c, error_7c_7, marker = "v", s = 5, c = "orangered", label = "Zero-level $\\times$ 7")
plt.plot(x,fit_func(x, popt_7c_7[0]), c = "orangered", label = "Zero-level $\\times$ 7")

plt.plot(x, 28 * x ** 2, c = "g", label = "$T \\times 8$ Distillation")
# plt.plot(x, 1-(1-x) ** 7, c = "g", label = "$T \\times 7$")

plt.xlim(1e-4,1e-2)
plt.ylim(1e-7,1e-1)
plt.grid()
plt.xlabel("Physical Error Rate")
plt.ylabel("Logical Error Rate")
plt.legend(fontsize="x-small", loc="lower right")

plt.savefig("error_rate.png", dpi = 500)