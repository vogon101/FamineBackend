data {
  int<lower=0> K;
  int<lower=0> N;
  real y[N];
}
parameters {
  real alpha;
  real beta[K];
  real gamma;
  real<lower=0> sigma;
}
model {
  for (n in (K+1):N) {
    real mu = alpha + gamma*n;
    for (k in 1:K)
      mu += beta[k] * y[n-k];
    y[n] ~ normal(mu, sigma);
  }
}