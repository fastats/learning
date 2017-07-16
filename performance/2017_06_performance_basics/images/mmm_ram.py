import os
import matplotlib.pyplot as plt

print('PID: ', str(os.getpid()))
naive_data =[16843164, 17095332, 16924717, 16529307, 16284980]

ram_data = [10213817, 10278712, 10360700, 10374979, 10247666]

cache_data = [4608438, 4541536, 4732902, 4578372, 4666115]
cache_O1_data = [2555696, 2563074, 2590026, 2608439, 2586387]
cache_O2_data = [2071236, 2080014, 2075915, 2101009, 2087962]

reg_data = [4647602, 4679936, 4873517, 4825128, 4893849]
reg_O1_data = [1482011, 1496331, 1509257, 1492973, 1473843]


def mean(x): return sum(x) / len(x)


# Line plot
#
# plt.plot(naive_data, label='Naive MMM')
# plt.plot(ram_data, label='Ram MMM')
# plt.plot(cache_data, label='Cache MMM')
# plt.plot(cache_O1_data, label="Cache MMM (O1)")
# plt.plot(cache_O2_data, label="Cache MMM (O2)")

# plt.plot(reg_data, label='Reg MMM')
# plt.xlabel('Repeats')
# plt.ylabel('Clock cycles')
# plt.legend(loc='upper right')
# plt.show()

# Bar plot
#
plt.bar((0, 1), (mean(cache_data), mean(cache_O1_data)), width=0.35, label='Cache MMM')
plt.bar((0.35, 1.35), (mean(reg_data), mean(reg_O1_data)), width=0.35, label='Reg MMM')
plt.legend(loc='upper right')
plt.xticks((0.17,1.17), ('O0', 'O1'))
plt.xlabel('Optimisation Level')
plt.ylabel('Clock cycles')

plt.show()