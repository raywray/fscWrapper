import os

def extract_all_max_lhoods(num_of_sims, prefix, output_dir_path):
    results = []

    for i in range(1, num_of_sims + 1):
        best_lhoods_file_path = f"{output_dir_path}{prefix}_run_{i}_output/run_1/{prefix}/{prefix}.bestlhoods"

        # check if file exists (it won't if params are bad or the cluster didn't run)
        if os.path.exists(best_lhoods_file_path):
            # find best lhood & add to results
            with open(f"{best_lhoods_file_path}", "r") as f:
                header = next(f).split()
                max_est_index = header.index("MaxEstLhood")
                values = next(f).split()
                max_est_lhood = values[max_est_index]
                results.append((i, max_est_lhood))

    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    return sorted_results

def get_overall_best_model(results, output_dir_path):

    with open(f"{output_dir_path}best_lhoods_results.txt", "w") as f:
        for result in results:
            f.write(f"{result[0]} {result[1]}\n")
    if not results:
        best_fit_run = "NA"
    else:
        best_fit_run = results[0][0]
    return best_fit_run

out_dir = "/home/resplin5072/output/fsc_output"
all_max_results = extract_all_max_lhoods(1000, "hops", out_dir)
best_fit_run = get_overall_best_model(all_max_results, out_dir)
print("best fit run: ", best_fit_run)