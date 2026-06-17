import numpy as np

def logical_std_calc(shots, logical_error_rate, success_rate):
    accepted = shots * success_rate
    return np.sqrt(logical_error_rate * (1 - logical_error_rate) / accepted)

def success_rate_std_calc(shots, success_rate):
    return np.sqrt(success_rate * (1 - success_rate) / shots)

result = [
    [5e6, 0.0002703683888719046, 0.418688],
    [5e6, 0.00019523066744384006, 0.4978726],
    [5e6, 0.00010763579824934929, 0.5927396],
    [5e6, 4.65009456137416e-05, 0.705362],
    [5e6, 1.1667975146736694e-05, 0.8399058],
    [5e6, 3.1638657726672983e-06, 0.9166002]
]

logical_error_rate_std_grown = []
success_rate_std_grown = []

for shots, logical_error_rate, success_rate in result:
    logical_std = logical_std_calc(shots, logical_error_rate, success_rate)
    success_rate_std = success_rate_std_calc(shots, success_rate)
    logical_error_rate_std_grown.append(logical_std)
    success_rate_std_grown.append(success_rate_std)

print(logical_error_rate_std_grown)
print(success_rate_std_grown)