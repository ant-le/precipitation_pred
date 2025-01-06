import pandas as pd
import numpy as np

def split_data(df:pd.DataFrame, split:float=0.7):
    df = df.set_index('date')
    idx_to_split = round(len(df.index) * split)

    train = df.iloc[:idx_to_split]
    test = df.iloc[idx_to_split:]

    y_train = train.prec
    y_test = test.prec

    # Exogenous variables
    drop_cols =['prec']
    X_train = train.drop(columns=drop_cols)
    X_test = test.drop(columns=drop_cols)

    return X_train, y_train, X_test, y_test


def get_errors(pred:np.array, truth:np.array):
    assert pred.shape == truth.shape
    diff = pred - truth
    N = pred.shape[0]
    rmse = np.sqrt(np.sum(diff ** 2)/N)
    abse = np.sum(np.abs(diff)) / N
    
    return {'RMSE': float(rmse), 'Abs Error':float(abse)}