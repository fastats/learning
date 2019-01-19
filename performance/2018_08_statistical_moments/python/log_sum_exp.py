import numpy as np
from numba import njit


@njit
def streaming_stable_log_sum_exp(data):

    # forgo checking dims / size etc etc

    # initial state
    max_data = data[0]
    sum_exp = 1

    for i in range(1, data.size):  # hence streaming nature
        data_i = data[i]

        if data_i <= max_data:
            # new value not bigger than max_data
            sum_exp += np.exp(data_i - max_data)
        else:
            # new value bigger than max_data
            sum_exp = sum_exp * np.exp(max_data - data_i) + 1
            max_data = data_i

    return np.log(sum_exp) + max_data


@njit
def stable_log_sum_exp(data):
    max_data = np.max(data)
    return np.log(np.sum(np.exp(data - max_data))) + max_data
