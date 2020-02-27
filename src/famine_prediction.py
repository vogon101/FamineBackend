import numpy as np
import scipy.special
import scipy.stats

from FamineStore import FamineStore


def predict_famine(fit, predicted_data):
    all_coeffs = list(map(lambda x: sum(x) / len(x), fit.get_posterior_mean()))
    times = sorted(predicted_data.keys())
    print(times)
    nFeatures = len(predicted_data[times[0]]['features'])
    al_2, be_2, co_2, k_2 = all_coeffs[0], all_coeffs[1:4], all_coeffs[4:4 + nFeatures], all_coeffs[4 + nFeatures]
    al_3, be_3, co_3, k_3 = all_coeffs[5 + nFeatures], all_coeffs[6 + nFeatures:9 + nFeatures], all_coeffs[
                                                                                                9 + nFeatures:9 + 2 * nFeatures], \
                            all_coeffs[9 + 2 * nFeatures]
    al_4, be_4, co_4, k_4 = all_coeffs[10 + 2 * nFeatures], all_coeffs[
                                                            11 + 2 * nFeatures:14 + 2 * nFeatures], all_coeffs[
                                                                                                    14 + 2 * nFeatures:14 + 3 * nFeatures], \
                            all_coeffs[14 + 3 * nFeatures]

    prev_P2 = None
    prev_P3 = None
    prev_P4 = None

    predictions = dict()
    for (i, time) in enumerate(times):

        if ('P2' not in predicted_data[time]):
            prediction = dict()
            features = predicted_data[time]['features']
            P2_mean = scipy.special.expit(
                al_2 + be_2[0] * scipy.special.logit(prev_P2) + be_2[1] * scipy.special.logit(prev_P3) + be_2[
                    2] * scipy.special.logit(prev_P4) + sum(np.multiply(co_2, features)))
            P3_mean = scipy.special.expit(
                al_3 + be_3[0] * scipy.special.logit(prev_P2) + be_3[1] * scipy.special.logit(prev_P3) + be_3[
                    2] * scipy.special.logit(prev_P4) + sum(np.multiply(co_3, features)))
            P4_mean = scipy.special.expit(
                al_4 + be_4[0] * scipy.special.logit(prev_P2) + be_4[1] * scipy.special.logit(prev_P3) + be_4[
                    2] * scipy.special.logit(prev_P4) + sum(np.multiply(co_4, features)))

            P2_a, P2_b = P2_mean * k_2, (1 - P2_mean) * k_2
            P3_a, P3_b = P2_mean * k_3, (1 - P3_mean) * k_3
            P4_a, P4_b = P2_mean * k_4, (1 - P4_mean) * k_4

            P2_95 = (scipy.stats.beta.ppf(0.025, P2_a, P2_b), scipy.stats.beta.ppf(0.975, P2_a, P2_b))
            P2_68 = (scipy.stats.beta.ppf(0.16, P2_a, P2_b), scipy.stats.beta.ppf(0.84, P2_a, P2_b))
            prediction['P2'] = {'mean': P2_mean, '95': P2_95, '68': P2_68}

            P3_95 = (scipy.stats.beta.ppf(0.025, P3_a, P3_b), scipy.stats.beta.ppf(0.975, P3_a, P3_b))
            P3_68 = (scipy.stats.beta.ppf(0.16, P3_a, P3_b), scipy.stats.beta.ppf(0.84, P3_a, P3_b))
            prediction['P3'] = {'mean': P3_mean, '95': P3_95, '68': P3_68}

            P4_95 = (scipy.stats.beta.ppf(0.025, P4_a, P4_b), scipy.stats.beta.ppf(0.975, P4_a, P4_b))
            P4_68 = (scipy.stats.beta.ppf(0.16, P4_a, P4_b), scipy.stats.beta.ppf(0.84, P4_a, P4_b))
            prediction['P4'] = {'mean': P4_mean, '95': P4_95, '68': P4_68}

            prev_P2 = P2_mean
            prev_P3 = P3_mean
            prev_P4 = P4_mean

            predictions[time] = prediction

        else:
            prev_P2 = max(1e-5, predicted_data[time]['P2'])
            prev_P3 = max(1e-5, predicted_data[time]['P3'])
            prev_P4 = max(1e-5, predicted_data[time]['P4'])
    return predictions


if __name__ == "__main__":
    store = FamineStore()
    # print(store.per_region_model["Awdal"].fit.fit)

    # print(store.per_region_pred_data["Awdal"]["ipc_df"])

    #predict_famine(store.per_region_model["Awdal"].fit.fit, store.per_region_pred_datasets["Awdal"])
