from FamineStore import FamineStore
import os


def predict_famine(fit, predicted_data, nqs, iterations):
    print(predicted_data.keys())

if __name__ == "__main__":
    os.chdir("..")
    store = FamineStore()
    print(store.per_region_model["Awdal"].fit.fit)

    print(store.per_region_pred_data["Awdal"]["ipc_df"])

    predict_famine(store.per_region_model["Awdal"].fit.fit, store.per_region_pred_datasets["Awdal"], 6, 1000)