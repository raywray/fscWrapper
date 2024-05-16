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
    path_to_aic = "/home/raya/Documents/Projects/fscWrapper/utilities/calculateAIC.sh"
    os.chdir(path_to_best_max_est_run)
    os.system(f"{path_to_aic} {prefix}")

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

max_est_run_path = "/home/raya/Documents/Projects/fscWrapper/output/fsc_output/hops_run_1_output/run_1/hops"
prefix = "hops"

# model_comp_with_aic(max_est_run_path, prefix)
visualize_best_fit_model(max_est_run_path, prefix)