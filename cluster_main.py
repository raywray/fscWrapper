import os
import sys

from utilities import use_fsc, run_model_in_fsc  # type: ignore


def create_directory(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def run_setup(cur_run, output_dir, project_path, prefix):
    # make directory
    run_output_folder = os.path.join(output_dir, f"run_{cur_run}")
    create_directory(run_output_folder)

    # copy SFS into new dir
    os.system(f"cp {project_path}/{prefix}*.obs {run_output_folder}")

    # copy .tpl and .est into new dir
    os.system(f"cp {output_dir}/{prefix}* {run_output_folder}")

    # move into new dir
    os.chdir(run_output_folder)

def run(output_dir, project_path, prefix, cur_run):
    # first, add fsc to project path
    use_fsc.add_fsc_to_path(project_path)

    # setup the run
    run_setup(
        cur_run=cur_run, output_dir=output_dir, project_path=project_path, prefix=prefix
    )

    # NOTE: commenting these out because it results in a segmentation fault. FSC should be run in the folder anyways, so it shouldn't matter
    # tpl_file_path = os.path.join(output_dir, f"run_{cur_run}", f"{prefix}.tpl")
    # est_file_path = os.path.join(output_dir, f"run_{cur_run}", f"{prefix}.est")
    tpl_filename = f"{prefix}.tpl"
    est_filename = f"{prefix}.est"
    
    # run in fsc
    run_model_in_fsc.send_model_to_fsc(tpl_filename=tpl_filename, est_filename=est_filename, sfs_type="d") # the d is hardcoded here


if __name__ == "__main__":
    # get user params
    # example call: python3 cluster_main.py output_directory/ fscWrapper_project_path/ hops random.tpl random.est 3
    if len(sys.argv) < 2:
        print("Usage: python script.py <parameter>")
        sys.exit(1)
    output_dir = sys.argv[1]
    project_path = sys.argv[2]
    prefix = sys.argv[3]
    cur_run = sys.argv[4]

    # run program
    run(
        output_dir=output_dir,
        project_path=project_path,
        prefix=prefix,
        cur_run=cur_run,
    )
