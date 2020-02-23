data {
    int<lower=0> N;
    int<lower=0> K;
    matrix[N, K] feats;
    vector[N] response;
}
parameters{
    real alpha;
    real beta;
    vector[K] coeffs;
    real<lower=0> sigma;
}
model {
    response[2:N] ~ normal(alpha + beta*response[1:(N-1)] + feats[2:N]*coeffs, sigma);
    coeffs ~ normal(0, 1);
}