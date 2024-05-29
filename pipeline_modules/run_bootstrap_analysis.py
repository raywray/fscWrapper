import os
import re

def extract_best_run(output_dir, prefix):
    best_lhoods_txt_path = os.path.join(output_dir, "best_lhoods_results.txt")
    with open(best_lhoods_txt_path, "r") as f:
        first_line = f.readline().strip()
    best_run_pattern = re.compile(r'(\d+):(\d+)')
    match = best_run_pattern.search(first_line)
    if match:
        simulation_group = match.group(1)
        run = match.group(2)
    else:
        print("No match found")
    
    new_best_run_folder = os.path.join(output_dir, "best_run")
    
    if not os.path.exists(new_best_run_folder):
        os.makedirs(new_best_run_folder)
        path_to_best_run = os.path.join(output_dir, f"{prefix}_run_{simulation_group}_output/run_{run}")
        os.system(f"cp -r {path_to_best_run}/* {new_best_run_folder}")
    
    return new_best_run_folder

def model_comp_with_aic(path_to_best_max_est_run, prefix):
    # the folder in the path must have the .bestlhoods and the .est (might have to move the .est in manually)
    # output is saved as {prefix}.AIC
    """
    cd bestrun/
    calculateAIC.sh early_geneflow

    # Usage: calculateAIC.sh modelprefix
    # This script calculates AIC from fsc modeling results
    # Run in the folder with the highest likelihood
    """

    # move in est file to the /prefix dir
    est_file_path = os.path.join(path_to_best_max_est_run, f"{prefix}.est")
    best_run_prefix_folder = os.path.join(path_to_best_max_est_run, f"{prefix}")

    os.system(f"cp {est_file_path} {best_run_prefix_folder}")

    # run the aic
    path_to_aic = "/Users/raya/Documents/School/fscWrapper/utilities/calculateAIC.sh"
    os.chdir(best_run_prefix_folder)
    os.system(f"{path_to_aic} {prefix}")
    # the output will the in the working directory under {prefix}.AIC

def visualize_best_fit_model(path_to_best_run, prefix):
    # the .tpl has to be in this folder, as well as the .obs sfs's
    """
    SFStools.r -t print2D -i early_geneflow
    plotModel.r -p early_geneflow -l NyerMak,PundMak    
    """
    # move tpl into folder
    tpl_file_path = os.path.join(path_to_best_run, f"{prefix}.tpl")
    best_run_prefix_folder = os.path.join(path_to_best_run, f"{prefix}")
    os.system(f"cp {tpl_file_path} {best_run_prefix_folder}")

    # move .obs to folder
    obs_file_path = os.path.join(path_to_best_run, f"{prefix}*.obs")
    os.system(f"cp {obs_file_path} {best_run_prefix_folder}")

    # define paths
    path_to_sfs_tools = "/Users/raya/Documents/School/fscWrapper/utilities/SFStools.r"
    path_to_plot_model = "/Users/raya/Documents/School/fscWrapper/utilities/plotModel.r"
    best_run_full_path = os.path.join(path_to_best_run, prefix)

    os.chdir(best_run_full_path)

    # run sfs tools: NOTE: this does not work, but idk how to fix it
    os.system(f"{path_to_sfs_tools} -t print2D -i {prefix}")
    # run plot model 
    os.system(f"{path_to_plot_model} -p {prefix} -l pop0,pop1,pop2,pop3")

    return


output_dir = "/Users/raya/Documents/School/fscWrapper/output/fsc_output"
prefix = "hops"
max_est_run_path = extract_best_run(output_dir, prefix)

# model_comp_with_aic(max_est_run_path, prefix)
visualize_best_fit_model(max_est_run_path, prefix)