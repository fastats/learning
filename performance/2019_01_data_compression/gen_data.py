
from datetime import date, timedelta

import numpy as np
import pandas as pd


IDENT_BASE = "ABC"


def gen_identifiers(n=3000):
    return [IDENT_BASE + str(x).zfill(6)
            for x in range(n)]


def gen_dates(n=3000):
    today = date.today()
    start = today - timedelta(days=n)
    return pd.date_range(start, today)


def gen_data():
    ids = gen_identifiers()
    dates = gen_dates()
    data = np.random.random(len(ids))

    results = []
    for date in dates:
        df = pd.DataFrame({
            'identifier': ids,
            'value': data
        })
        df['date'] = date
        results.append(df)

    return pd.concat(results)


if __name__ == '__main__':
    df = gen_data()
    print(f'DataFrame: {df.shape}')
    df.to_hdf('initial.h5', key='df')