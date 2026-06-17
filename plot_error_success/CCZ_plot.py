import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit 
try:
    import scienceplots
    PLOT_STYLE = ["science", "ieee"]
except ModuleNotFoundError:
    PLOT_STYLE = "default"

prob_list = [1e-3, 8e-4, 6e-4, 4e-4, 2e-4, 1e-4]
logical_error_rate_ungrown = [0.0002703683888719046, 0.00019523066744384006, 0.00010763579824934929, 4.65009456137416e-05, 1.1667975146736694e-05, 3.1638657726672983e-06]
success_rate_ungrown = [0.418688, 0.4978726, 0.5927396, 0.705362, 0.8399058, 0.9166002]
logical_error_rate_std_ungrown = [1.1362894640086647e-05, 8.854978406193676e-06, 6.026123395572438e-06, 3.6310293778435086e-06, 1.6668438679594455e-06, 8.308705429272706e-07]
success_rate_std_ungrown = [0.00022063016958521336, 0.00022360477372777174, 0.00021972681520098544, 0.00020387567238687405, 0.00016399027234952686, 0.0001236481082426739]

logical_error_rate_grown = [0.00034852566383247535, 0.0002219381364258208, 0.00011960131162771752, 5.422499759000011e-05, 1.3586052894515038e-05, 3.866977783985162e-06]
success_rate_grown = [0.275446, 0.3568562, 0.4615334, 0.5975104, 0.7728514, 0.8792396]
logical_error_rate_std_grown = [3.556505232335755e-05, 1.1151573302085898e-05, 7.1987224382979435e-06, 4.2602026578644015e-06, 1.3258539944309626e-06, 6.6317993647621e-07]
success_rate_std_grown = [0.0004467387391798477, 0.00021424745157016923, 0.00022294408298245547, 0.000219313347469706, 0.0001324960805148741, 0.00010304238244132363]

# logical_error_rate_0per = []
# expansion_error_0per = [4.591e-05, 2.328e-05, 9.618e-06, 2.868e-06, 3.290e-07, 5.000e-08]
# for i in range(6):
#     logical_error_rate_0per.append(1- ((1 - logical_error_rate[i]) * (1 - expansion_error_0per[i])**6))

# prob_3d = [1e-3, 7e-4, 5e-4, 3e-4, 1e-4]
# suc_3d = [0.7031721, 0.7814325, 0.8382618, 0.89949474, 0.96529446]
# for i in range(len(suc_3d)):
#     suc_3d[i] = suc_3d[i]**7


def fit_func(x,a):
    return a * x**2

# for i in prob_list:
#     e, s = zero_ccz(i, 10**7)
#     logical_error_rate.append(e)
#     success_rate.append(s)

# print(logical_error_rate)
# print(success_rate)

popt, pcov = curve_fit(fit_func, prob_list, logical_error_rate_ungrown)
print(popt)
popt2, pcov2 = curve_fit(fit_func, prob_list, logical_error_rate_grown)
print(popt2)



plt.style.use(PLOT_STYLE)
plt.xscale('log')
plt.yscale('log')
x = np.linspace(1e-4,1e-2,2000)

plt.errorbar(prob_list, logical_error_rate_ungrown, yerr=logical_error_rate_std_ungrown,
             fmt=".", markersize=4, capsize=2, elinewidth=0.6, color="r", label="Ungrown")
plt.plot(x,fit_func(x, popt[0]),c = "r", label = "Ungrown")
plt.errorbar(prob_list, logical_error_rate_grown, yerr=logical_error_rate_std_grown,
             fmt="x", markersize=4, capsize=2, elinewidth=0.6, color="b", label="Grown")
# plt.scatter(expansion_1e3_physical, expansion_1e3, marker = ".", s = 10, c = "r", label = "Zero-level_CCZ")
# plt.scatter(1e-3, expansion_1e3[2], marker = ".", s = 10, c = "r", label = "Zero-level_CCZ")
plt.plot(x,fit_func(x, popt2[0]),c = "b", label = "Grown")

# plt.plot(x,1-(1-100*x**2)**7,c = "b", label = "$7ZLD$")
plt.plot(x, 1-(1-x)**7,c = "g", label = "$T \\times 7$")

plt.xlim(1e-4,1e-2)
plt.ylim(1e-6,1e-1)
plt.grid()
plt.xlabel("Physical Error Rate")
plt.ylabel("Logical Error Rate")
plt.legend(fontsize="x-small", loc="lower right")

plt.savefig("error_rate.pdf")

plt.clf()

plt.style.use(PLOT_STYLE)
plt.xscale('log')
# plt.yscale('log')
plt.errorbar(prob_list, success_rate_ungrown, yerr=success_rate_std_ungrown,
             fmt=".", markersize=4, capsize=2, elinewidth=0.6, color="r", label="Ungrown")
plt.errorbar(prob_list, success_rate_grown, yerr=success_rate_std_grown,
             fmt="x", markersize=4, capsize=2, elinewidth=0.6, color="b", label="Grown")
# plt.scatter(prob_3d, suc_3d, marker = "x", s = 10, c = "b", label = "7ZLD")
plt.xlim(1e-4,1e-2)
plt.ylim(0, 1)
plt.grid()
plt.xlabel("Physical Error Rate")
# plt.ylabel("Discard Rate")
plt.ylabel("Success Rate")
plt.legend(fontsize="x-small")
plt.savefig("success_rate.pdf")
# plt.savefig("discard_rate.png", dpi = 500)