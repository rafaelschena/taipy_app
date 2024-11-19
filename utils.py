import pandas as pd

def load_data_naval_pdm():

    features = [
    'lp',
    'v',
    'GTT',
    'GTn',
    'GGn',
    'Ts',
    'Tp',
    'T48',
    'T1',
    'T2',
    'P48',
    'P1',
    'P2',
    'Pexh',
    'TIC',
    'mf',
    'kMc',
    'kMt'
    ]

    df = pd.read_csv('./data/data.txt', sep='   ', names=features, engine='python')

    return df

