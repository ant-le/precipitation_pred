from cmdstanpy import CmdStanModel, install_cmdstan
import pandas as pd
import numpy as np


class HierarchicalModel:
    def __init__(self, n_lags: int = 1, n_season: int = 2):
        self.n_lags = n_lags
        self.n_season = n_season
        self.params = None

    def fit(self, data: pd.DataFrame, exog_vars: list):
        self.exog = exog_vars
        self.regions = data.index.get_level_values(3).unique()
        self.scale = data.groupby('region')[self.exog].agg(['mean', 'std'])
        stan_df = self._prepare_data(data)
        fit = self._run_model(stan_df)
        return fit

    def predict(self, data: pd.DataFrame):
        stan_df = self._prepare_data(data)

        alpha_samples = self.variables.get('alpha')
        beta_samples = self.variables.get('beta')
        phi_samples = self.variables.get('phi')
        gamma_samples = self.variables.get('gamma')
        delta_samples = self.variables.get('delta')

        alpha_mean = np.mean(alpha_samples, axis=0)
        beta_mean = np.mean(beta_samples, axis=0)
        phi_mean = np.mean(phi_samples, axis=0)
        gamma_mean = np.mean(gamma_samples, axis=0)
        delta_mean = np.mean(delta_samples, axis=0)

        T = stan_df.get('T')
        R = stan_df.get('R')
        p = stan_df.get('p')
        J = stan_df.get('J')
        X = stan_df.get('X')

        y_pred_mean = np.zeros((R, T - p))

        for r in range(R):
            for t in range(p, T):
                ar_effect = 0
                seasonal_effect = 0

                for k in range(1, p+1):
                    ar_effect += phi_mean[k - 1] * y_pred_mean[r, t - k - 1]

                for j in range(J):
                    seasonal_effect += gamma_mean[j] * np.sin(2 * np.pi * j * t / 365) + \
                        delta_mean[j] * np.cos(2 * np.pi * j * t / 365)

                linear_effect = np.dot(beta_mean, X[r, t])

                mu_t = alpha_mean[r] + ar_effect + \
                    seasonal_effect + linear_effect

                y_pred_mean[r, t - p] = np.exp(mu_t) - 1

        y = np.exp(stan_df.get('y')) - 1
        return y_pred_mean, y[:, self.n_lags:]

    def load(self, name: str):
        self.params = pd.read_csv(
            f'src/outputs/{name}_params.csv', index_col=0)
        self.scale = pd.read_csv(
            f'src/outputs/{name}_scale.csv', index_col=0, header=[0, 1])
        self.variables = np.load(
            f'src/outputs/{name}_variables.npy', allow_pickle=True).item()
        self.exog = list(self.scale.stack(
            future_stack=True).columns.difference(['prec']))
        self.regions = list(self.scale.index)
        self.n_lags = self.variables.get('phi').shape[1]
        self.n_seasons = self.variables.get('gamma').shape[1]
        print('Parameters loaded sucessfully!')

    def save(self, name: str):
        if type(self.params) is pd.DataFrame and type(self.scale) is pd.DataFrame:
            self.params.to_csv(f'src/outputs/{name}_params.csv')
            self.scale.to_csv(f'src/outputs/{name}_scale.csv')
            np.save(f'src/outputs/{name}_variables.npy', self.variables)
            print('Parameters saved sucessfully!')

    def _run_model(self, data):
        install_cmdstan()

        model = CmdStanModel(stan_file="src/model_b.stan")

        fit = model.sample(
            data=data,
            iter_warmup=50,
            iter_sampling=50,
            chains=4,
            parallel_chains=4,
            seed=10,
        )
        self.variables = fit.stan_variables()
        self.params = fit.summary()
        return fit

    def _prepare_data(self, data):
        data['time_index'] = (data['date'] - data['date'].min()).dt.days

        T = data.time_index.nunique()
        R = len(self.regions)
        P = len(self.exog)
        X = np.zeros((R, T, P))
        y = np.zeros((R, T))

        for i, region in enumerate(self.regions):
            region_data = data[data.index.get_level_values(
                3) == region].sort_values('time_index')

            region_scales = self.scale.loc[region]
            means = region_scales.xs('mean', level=1, axis=0)
            stds = region_scales.xs('std', level=1, axis=0)
            region_data_scaled = (region_data[self.exog] - means) / stds
            X[i, :, :] = region_data_scaled[self.exog].values
            y[i, :] = np.log(region_data['prec'].values + 1)

        data = {
            "T": T,                      # Number of time points (days)
            "R": R,                      # Number of regions
            "P": P,                      # Number of predictors
            "p": self.n_lags,            # Number of Autoregressive Features
            "X": X,                      # Predictor matrix
            "y": y,                      # Response matrix
            # Number of Fourier terms (for seasonality)
            "J": self.n_season
        }

        return data
