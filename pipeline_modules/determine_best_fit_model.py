def find_lhoods(num_of_sims):
    results = []

    for i in range(1, num_of_sims + 1):
        best_lhoods_filepath = f"output/run_{i}/run_{i}.bestlhoods"  # TODO change the run_{i}.best... to random

        with open(f"{best_lhoods_filepath}", "r") as best_lhoods_file:
            for line in best_lhoods_file:
                if "MaxEstLhood" not in line:
                    parts = line.split()
                    max_est_lhood_index = 3
                    results.append((i, float(parts[max_est_lhood_index])))

    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    return sorted_results


def get_best_fit_model(results):
    with open("best_lhood_results.txt", "w") as results_file:
        for result in results:
            results_file.write(f"{result[0]} {result[1]}\n")
    best_fit_run = results[0][0]
    return best_fit_run


def get_best_lhoods(num_of_sims):
    best_lhood_resuls = find_lhoods(num_of_sims)
    best_fit_run = get_best_fit_model(best_lhood_resuls)

    return best_fit_run
