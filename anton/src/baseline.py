import torch
from pandas import DataFrame, Series


class Linear_Baseline:
    def __init__(self, n_lags: int = 3, n_regions: int = 100, intercept: bool = False):
        self.n_regions = n_regions
        self.n_lags = n_lags
        self.intercept = intercept

    def fit(self, exog: DataFrame, outcome: Series):
        self.seansanal_trends = outcome.groupby(level=(1, 2, 3)).agg('mean')
        X, y = self._prepare_data(exog, outcome)

        if y.ndim == 1:
            y = y.unsqueeze(1)

        if self.intercept:
            X = torch.cat([torch.ones(X.size(0), 1), X], dim=1)

        XtX_inv = torch.linalg.inv(X.T @ X)
        self.beta = XtX_inv @ X.T @ y

    def predict(self, exog: DataFrame, outcome: Series):
        X, y = self._prepare_data(exog, outcome)

        if self.intercept:
            X = torch.cat([torch.ones(X.size(0), 1), X], dim=1)

        pred = (X @ self.beta.squeeze()).squeeze()
        pred[pred < 0] = 0

        return pred.numpy(), y.numpy()

    def _prepare_data(self, exog, outcome):
        X = torch.Tensor(exog.merge(self.seansanal_trends, on=[
                         'month', 'day', 'region'], how='left').values)
        y = torch.Tensor(outcome.values)
        if self.n_lags > 0:
            lagged_outcome = torch.stack(
                [y.roll(self.n_regions*lag) for lag in range(1, self.n_lags+1)]).T
            X_full = torch.concat([X, lagged_outcome], dim=1)

            X = X_full[self.n_lags*self.n_regions:, :]
            y = y[self.n_lags*self.n_regions:]

        return X, y
