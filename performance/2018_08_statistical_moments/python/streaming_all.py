
import numpy as np
import pandas as pd
import scipy.stats
from numba import njit


def naive_all_stats(data: pd.DataFrame):

    # initialise output data structures
    covariances, variances, std, mean, correlations, skewness, kurtosis = initialise_outputs(data.values)
    n_periods = data.shape[0]

    # naive rescan of each window using Pandas and Scipy to generate stats
    for i in range(n_periods):
        window_data = data.iloc[:i + 1, :]
        covariances[i] = window_data.cov().values
        variances[i] = window_data.var().values
        std[i] = window_data.std().values
        mean[i] = window_data.mean().values
        correlations[i] = window_data.corr().values
        skewness[i] = scipy.stats.skew(window_data.values)
        kurtosis[i] = scipy.stats.kurtosis(window_data.values)

    return {
        'covariances': covariances,
        'variances': variances,
        'std': std,
        'mean': mean,
        'correlations': correlations,
        'skewness': skewness,
        'kurtosis': kurtosis,
    }


def streaming_all_stats(returns: pd.DataFrame):
    covariances, variances, std, mean, correlations, skewness, kurtosis = streaming_all_stats_inner(returns.values)
    return {
        'covariances': covariances,
        'variances': variances,
        'std': std,
        'mean': mean,
        'correlations': correlations,
        'skewness': skewness,
        'kurtosis': kurtosis,
    }


@njit
def empty_vector(n_periods, n_assets):
    return np.empty((n_periods, n_assets))


@njit
def empty_array(n_periods, n_assets):
    return np.empty((n_periods, n_assets, n_assets))


@njit
def update_S(S, M2, delta, delta_n):

    # update diagonal terms
    np.fill_diagonal(S, M2)

    # populate off diagonal terms
    for col_idx, row_idx in np.ndindex(S.shape):

        # lower diagonal
        if col_idx < row_idx:
            S[col_idx, row_idx] += delta[col_idx] * (delta - delta_n)[row_idx]

        # upper diagonal - exploit symmetry
        elif col_idx > row_idx:
            S[col_idx, row_idx] = S[row_idx, col_idx]


@njit
def initialise_outputs(data):
    n_periods, n_assets = data.shape

    # initialise output arrays
    covariances = empty_array(n_periods, n_assets)
    correlations = empty_array(n_periods, n_assets)

    # initialise output vectors
    variances = empty_vector(n_periods, n_assets)
    std = empty_vector(n_periods, n_assets)
    mean = empty_vector(n_periods, n_assets)
    skewness = empty_vector(n_periods, n_assets)
    kurtosis = empty_vector(n_periods, n_assets)

    return covariances, variances, std, mean, correlations, skewness, kurtosis


@njit
def streaming_all_stats_inner(data):

    # initialise output data structures
    covariances, variances, std, mean, correlations, skewness, kurtosis = initialise_outputs(data)
    n_periods, n_assets = data.shape

    # initialise internal data structures
    M1 = np.zeros(n_assets)
    M2 = np.zeros(n_assets)
    M3 = np.zeros(n_assets)
    M4 = np.zeros(n_assets)
    S = np.zeros((n_assets, n_assets))

    for i in range(n_periods):
        data_i = data[i, :]  # data for period i, hence 'streaming' nature

        n = i + 1
        delta = data_i - M1
        delta_n = delta / n
        delta_n2 = delta_n * delta_n
        term_1 = delta * delta_n * i

        M4 += term_1 * delta_n2 * (n * n - 3 * n + 3) + 6 * delta_n2 * M2 - 4 * delta_n * M3
        M3 += term_1 * delta_n * (n - 2) - 3 * delta_n * M2
        M2 += term_1
        M1 += delta_n

        # first observation
        if i == 0:
            covariances[i] = np.full_like(S, fill_value=np.nan)
            correlations[i] = np.full_like(S, fill_value=np.nan)
            skewness[i] = np.zeros(n_assets)
            kurtosis[i] = np.full(n_assets, fill_value=-3.0)  # to replicate scipy behaviour

        # subsequent observations
        else:
            update_S(S, M2, delta, delta_n)
            covariances[i] = S / i
            skewness[i] = np.multiply(np.sqrt(n) * M3, np.power(M2, -1.5))
            kurtosis[i] = np.multiply(n * M4, np.power(M2, -2)) - 3

        variances[i] = np.diag(covariances[i])
        std[i] = np.sqrt(variances[i])
        mean[i] = M1

        if np.all(std[i] == 0):
            correlations[i] = np.ones_like(S)
        else:
            correlations[i] = np.divide(np.divide(covariances[i], std[i]).T, std[i])

    return covariances, variances, std, mean, correlations, skewness, kurtosis


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
