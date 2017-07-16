import os
import matplotlib.pyplot as plt

print('PID: ', str(os.getpid()))
data =[
    16843164,
    17095332,
    16924717,
    16529307,
    16284980
]

plt.plot(data, label='Naive MMM')
plt.xlabel('Repeats')
plt.ylabel('Clock cycles')
plt.legend(loc='upper right')
plt.show()