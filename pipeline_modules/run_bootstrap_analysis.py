import os

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
    # the .tpl has to be in this folder
    """
    SFStools.r -t print2D -i early_geneflow
    plotModel.r -p early_geneflow -l NyerMak,PundMak    
    """
    path_to_sfs_tools = "/home/raya/Documents/Projects/fscWrapper/utilities/SFStools.r"
    path_to_plot_model = "/home/raya/Documents/Projects/fscWrapper/utilities/plotModel.r"
    os.chdir(path_to_best_run)
    os.system(f"{path_to_sfs_tools} -t print2D -i {prefix}")
    # os.system(f"{path_to_plot_model} -p {prefix} -l NyerMak,PundMak")

    return

max_est_run_path = "/Users/raya/Documents/School/fscWrapper/output/fsc_output/hops_run_69_output/run_3"
prefix = "hops"

model_comp_with_aic(max_est_run_path, prefix)
# visualize_best_fit_model(max_est_run_path, prefix)