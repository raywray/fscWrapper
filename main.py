import os
from pipeline_modules import (
    generate_random_tpl,
    generate_random_est,
    determine_best_fit_model,
)

# User Provided Input
NUM_POPS = 3
SAMPLE_SIZES = [2, 4, 4]
MUTATION_RATE_DIST = {"min": 1e-7, "max": 1e-9, "type": "unif"}
EFFECTIVE_POP_SIZE_DIST = {"min": 100, "max": 300000, "type": "unif"}
RESIZED_DIST = {"min": 0, "max": 100, "type": "unif"}
ADMIX_DIST = {"min": 0, "max": 0.25, "type": "unif"}
MIGRATION_DIST = {"type": "logunif", "min": 1e-10, "max": 1e-1}
TIME_DIST = {
    "type": "unif",
    "single_max": 5000,
    "single_min": 1,
    "multiple_max": 600,
    "multiple_min": 1,
    "extra_max": 500,
    "extra_min": 0,
}

def execute_command(command):
    os.system(command)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def run_simluations(num_of_sims):
    # run x number of fsc simulations
    for i in range(1, num_of_sims + 1):
        # make & move to directory
        output_folder_name = f"output/run_{i}"
        os.mkdir(output_folder_name)
        os.chdir(output_folder_name)

        # TODO move other output files (sfs, etc.) to this directory

        # Create filenames
        tpl_filename = f"random_{i}.tpl"
        est_filename = f"random_{i}.est"

        # Generate random tpl & est files
        generate_random_tpl.generate_random_tpl_parameters(
            tpl_filename, NUM_POPS, SAMPLE_SIZES
        )
        generate_random_est.create_est(
            tpl_filename,
            est_filename,
            mutation_rate_dist=MUTATION_RATE_DIST,
            ne_dist=EFFECTIVE_POP_SIZE_DIST,
            resized_dist=RESIZED_DIST,
            admix_dist=ADMIX_DIST,
            time_dist=TIME_DIST,
            mig_dist=MIGRATION_DIST,
        )

        # Run fsc
        command = f"fsc28 -t {tpl_filename} -e {est_filename} -d -0 -C 10 -n 10000 -L 40 -s 0 -M"
        # execute_command(command) TODO uncomment when ready
        print("COMMAND: ", command)

        # go back to root directory
        os.chdir("../..")


def run():
    # Create output directory
    create_directory("output")
   
    num_of_sims = 10 # hard-coded, but can change
   
    # run simulations
    run_simluations(num_of_sims)
   
    # find the best fit run
    # best_fit_run = determine_best_fit_model.get_best_lhoods(num_of_sims)
    # print("best fit run: run", best_fit_run)


if __name__ == "__main__":
    run()
