data {
  int<lower=1> T;                // Number of time points (days)
  int<lower=1> R;                // Number of regions
  int<lower=1> P;                // Number of predictors
  int<lower=1> p;                // Order of the autoregressive process
  array[R] matrix[T, P] X;       // Predictors for each region
  matrix[R, T] y;                // Precipitation for each region
  int<lower=1> J;                // Number of Fourier terms
}

transformed data {

   matrix[T, J] time_harmonic_grid;
   for (t in 1:T) {
     for (j in 1:J) {
        time_harmonic_grid[t, j] = 2 * pi() * j * t / 365;
      }
   }

   array[R] matrix[T, J] seasonal_effects_sin = rep_array(sin(time_harmonic_grid), R);
   array[R] matrix[T, J] seasonal_effects_cos = rep_array(cos(time_harmonic_grid), R);
}

parameters {
  array[R] real alpha;           // Region-specific intercepts
  vector[P] beta;                // General coefficients
  vector[p] phi;                 // AR(p) coefficients
  array[R] real <lower=0.01> sigma;        // Noise standard deviation
  vector[J] gamma;               // Fourier sine coefficients
  vector[J] delta;               // Fourier cosine coefficients
}


model {
  // Priors
  alpha ~ normal(0,1);
  to_vector(beta) ~ normal(0, 1);
  phi ~ normal(0, 0.5);  
  gamma ~ normal(0, 0.1);
  delta ~ normal(0, 0.1);
  sigma ~ lognormal(0, 1);


  for (r in 1:R) {
    for (t in (p + 1):T) {
      real ar_effect = 0;
      real seasonal_effect = 0;
      
      // AR(p) component
      for (k in 1:p) {
        ar_effect += phi[k] * y[r][t - k];
      }
      seasonal_effect = dot_product(seasonal_effects_sin[r, t], gamma) +
                        dot_product(seasonal_effects_cos[r, t], delta);

      real mu_t = alpha[r] + ar_effect + dot_product(beta, X[r][t]) + seasonal_effect;
      y[r][t] ~ normal(mu_t, sigma[r]);
    }
  }
}
