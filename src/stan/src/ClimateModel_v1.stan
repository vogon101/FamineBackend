data {
    int<lower=0> J; // number of points
    vector[J] y; // temps
    vector[J] dates;
}
parameters {
    real k;
    real phase;
    real sigma;
    real offset;
    real m;
}
transformed parameters {

}
model {
    y ~ normal(k * sin(2 * 3.14159 * dates + phase) + offset, sigma);

}
/*
generated quantities {
    vector [J_pred] y_pred;
    for (i in 1:J_pred) {
        y_pred[i] = normal_rng(k * sin(2 * 3.14159 * pred_dates[i] + phase) + offset, sigma);
    }
}
*/