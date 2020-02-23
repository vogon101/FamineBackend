data {
    int<lower=0> N;
    int<lower=0> K;
    matrix[N,K] feats;
    vector[N] response_2;
    vector[N] response_3;
    vector[N] response_4;
}
transformed data {
    vector[N] logit_response_2;
    vector[N] logit_response_3;
    vector[N] logit_response_4;

    logit_response_2 = logit(response_2);
    logit_response_3 = logit(response_3);
    logit_response_4 = logit(response_4);
}
parameters{
    real alpha_2;
    vector[3] beta_2;
    vector[K] coeffs_2;
    real<lower = 100> kappa_2;

    real alpha_3;
    vector[3] beta_3;
    vector[K] coeffs_3;
    real<lower = 100> kappa_3;

    real alpha_4;
    vector[3] beta_4;
    vector[K] coeffs_4;
    real<lower = 100> kappa_4;
}

model{
    vector[N] mus_2;
    vector[N] mus_3;
    vector[N] mus_4;

    mus_2[2:N] = inv_logit(alpha_2 + beta_2[1]*logit_response_2[1:(N-1)] + beta_2[2]*logit_response_3[1:(N-1)] + beta_2[3]*logit_response_4[1:(N-1)] + feats[2:N]*coeffs_2);
    response_2[2:N] ~ beta_proportion(mus_2[2:N], kappa_2);

    mus_3[2:N] = inv_logit(alpha_3 + beta_3[1]*logit_response_2[1:(N-1)] + beta_3[2]*logit_response_3[1:(N-1)] + beta_3[3]*logit_response_4[1:(N-1)] + feats[2:N]*coeffs_3);
    response_3[2:N] ~ beta_proportion(mus_3[2:N], kappa_3);

    mus_4[2:N] = inv_logit(alpha_4 + beta_4[1]*logit_response_2[1:(N-1)] + beta_4[2]*logit_response_3[1:(N-1)] + beta_4[3]*logit_response_4[1:(N-1)] + feats[2:N]*coeffs_4);
    response_4[2:N] ~ beta_proportion(mus_4[2:N], kappa_4);
}