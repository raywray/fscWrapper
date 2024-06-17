import os

def extract_all_max_lhoods(num_models,num_sims, prefix, output_dir_path):
    results = []

    for i in range(num_models):
        for j in range(num_sims):
            # best_lhoods_file_path = f"{output_dir_path}{prefix}_run_{i+1}_output/run_{j+1}/{prefix}/{prefix}.bestlhoods"
            cur_model = f"{prefix}_random_model_{i+1}"
            cur_run = f"run_{j+1}"
            best_lhoods_file_path = os.path.join(output_dir_path, cur_model, cur_run, f"{prefix}/{prefix}.bestlhoods")

            # check if file exists (it won't if params are bad or the cluster didn't run)
            if os.path.exists(best_lhoods_file_path):
                # find best lhood & add to results
                with open(f"{best_lhoods_file_path}", "r") as f:
                    header = next(f).split()
                    max_est_index = header.index("MaxEstLhood")
                    max_obs_index = header.index("MaxObsLhood")
                    values = next(f).split()
                    max_est_lhood = float(values[max_est_index])
                    max_obs_lhood = float(values[max_obs_index])
                    difference = max_obs_lhood - max_est_lhood
                    if max_est_lhood != 0.0:
                        results.append((f"{cur_model}:{cur_run}", str(difference)))
    sorted_results = sorted(results, key=lambda x: float(x[1]))
    return sorted_results

def get_overall_best_model(results, output_dir_path):
    best_lhood_results_path = os.path.join(output_dir_path, "best_lhoods_results.txt")

    with open(best_lhood_results_path, "w") as f:
        for result in results:
            f.write(f"{result[0]} {result[1]}\n")
    if not results:
        best_fit_run = "NA"
    else:
        best_fit_run = results[0][0]
    return best_fit_run

local_out_dir = "/home/raya/Documents/Projects/output/fsc_output"
mesx_out_dir = "/usr/scratch2/userdata2/resplin5072/output/fsc_output"
prefix = "hops"

num_random_models = 10
num_sims_per_model = 10

all_max_results = extract_all_max_lhoods(num_random_models, num_sims_per_model, prefix, local_out_dir)
best_fit_run = get_overall_best_model(all_max_results, local_out_dir)
print("best fit run: ", best_fit_run)