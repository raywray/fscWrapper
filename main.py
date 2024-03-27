import os
from pipeline_modules import (
    generate_random_tpl,
    generate_random_est,
    determine_best_fit_model,
)
from utilities import get_user_params_from_yaml, use_fsc


def execute_command(command):
    os.system(command)


def create_directory(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def prepare_run(user_params, cur_run):
    # add fsc executable
    use_fsc.add_fsc_to_path()
    
    # make directory
    output_folder_name = f"output/run_{cur_run}"
    create_directory(output_folder_name)

    # copy SFS into new dir
    os.system(f"cp {user_params["FSC_INPUT_PREFIX"]}* {output_folder_name}")

    # move into new dir
    os.chdir(output_folder_name)


def run_simluations(user_params, num_of_sims):
    # run x number of fsc simulations
    for i in range(1, num_of_sims + 1):
        # prepare folder for run
        prepare_run(user_params, i)

        # Create filenames
        tpl_filename = f"{user_params["FSC_INPUT_PREFIX"]}.tpl"
        est_filename = f"{user_params["FSC_INPUT_PREFIX"]}.est"

        # Generate random tpl & est files
        generate_random_tpl.generate_random_tpl_parameters(
            tpl_filename, user_params["NUM_POPS"], user_params["SAMPLE_SIZES"]
        )
        generate_random_est.create_est(
            tpl_filename,
            est_filename,
            **user_params["MODEL_PARAMS"]
        )

        # Run fsc TODO: change so it runs each model 100 times
        # TODO: get best l hoods from this, compare each best with each best
        command = f"fsc28 -t {tpl_filename} -e {est_filename} -d -0 -C 10 -n 1000 -L 40 -s 0 -M"
        execute_command(command)

        # go back to root directory
        os.chdir("../..")


def run(user_params):
    # Create output directory
    create_directory("output")

    num_of_sims = 10  # TODO: hard-coded, but can change

    # run simulations
    run_simluations(user_params, num_of_sims)

    # find the best fit run
    best_fit_run = determine_best_fit_model.get_best_lhoods(num_of_sims, user_params["FSC_INPUT_PREFIX"])
    print("best fit run: run", best_fit_run)


if __name__ == "__main__":
    # get user params
    user_params = get_user_params_from_yaml.read_yaml_file("hops-input.yml")
    run(user_params)
