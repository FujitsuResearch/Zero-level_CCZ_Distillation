import numpy as np

def logical_std_calc(shots, logical_error_rate, success_rate):
    accepted = shots * success_rate
    return np.sqrt(logical_error_rate * (1 - logical_error_rate) / accepted)

def success_rate_std_calc(shots, success_rate):
    return np.sqrt(success_rate * (1 - success_rate) / shots)

result = [[1e6, 0.00034852566383247535, 0.275446],
          [5e6, 0.0002219381364258208, 0.3568562],
          [5e6, 0.00011960131162771752, 0.4615334],
          [5e6, 5.422499759000011e-05, 0.5975104],
          [1e7, 1.3586052894515038e-05, 0.7728514],
          [1e7, 3.866977783985162e-06, 0.8792396]]

logical_error_rate_std_grown = []
success_rate_std_grown = []

for shots, logical_error_rate, success_rate in result:
    logical_std = logical_std_calc(shots, logical_error_rate, success_rate)
    success_rate_std = success_rate_std_calc(shots, success_rate)
    logical_error_rate_std_grown.append(logical_std)
    success_rate_std_grown.append(success_rate_std)

print(logical_error_rate_std_grown)
print(success_rate_std_grown)