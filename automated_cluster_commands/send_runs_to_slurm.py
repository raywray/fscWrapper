import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utilities import generate_random_model, cluster_commands

"""DEFINE CONSTANTS"""
# local
isMacbook = False
if isMacbook:
    LOCAL_BASE_PATH = "/Users/raya/Documents/School/fscWrapper/"
else:
    LOCAL_BASE_PATH = "/home/raya/Documents/Projects/fscWrapper/"
SIMULATION_SUB_FOLDER = "fsc_output"
LOCAL_TEMPLATE_SLURM_FILE = os.path.join(
    LOCAL_BASE_PATH, "automated_cluster_commands", "slurm_template.sh"
)
LOCAL_OUT_DIR = os.path.join(LOCAL_BASE_PATH, "sim_output")
LOCAL_OUTPUT_SIM_DIR = os.path.join(LOCAL_OUT_DIR, SIMULATION_SUB_FOLDER)
LOCAL_OUTPUT_COMMANDS_DIR = os.path.join(LOCAL_OUT_DIR, "slurm_commands")
LOCAL_CLUSTER_CMDS_FILE = os.path.join(LOCAL_OUTPUT_COMMANDS_DIR, "cluster_cmds.txt")
LOCAL_SUBMIT_JOBS_SCRIPT = os.path.join(
    LOCAL_BASE_PATH, "automated_cluster_commands", "submit_all_slurm_jobs.sh"
)

# remote
REMOTE_BASE_PATH = "/rhome/respl001"
REMTOE_BASH_PROFILE_PATH = os.path.join(REMOTE_BASE_PATH, ".bash_profile")
REMOTE_OUTPUT_BASE_PATH = "/bigdata/armstronglab/respl001"
REMOTE_PROJECT_PATH = os.path.join(REMOTE_BASE_PATH, "Projects", "fscWrapper")
ME_AT_REMOTE_URL = "respl001@cluster.hpcc.ucr.edu"
REMOTE_CLUSTER_CMDS_DIR = os.path.join(REMOTE_OUTPUT_BASE_PATH, "cluster_commands")
REMOTE_RESULTS_OUTPUT_DIR = os.path.join(REMOTE_OUTPUT_BASE_PATH, "output")
REMOTE_SLURM_DESTINATION_DIR = os.path.join(
    REMOTE_CLUSTER_CMDS_DIR, SIMULATION_SUB_FOLDER
)
REMOTE_FSC_OUTPUT_DIR = os.path.join(REMOTE_RESULTS_OUTPUT_DIR, SIMULATION_SUB_FOLDER)

"""FUNCTIONS"""


def execute_command(command_list):
    command = " ".join(command_list)
    print(command)
    result = os.system(command)
    if result != 0:
        print("Command Failed to Execute")
    else:
        print("Command Successfully Executed")


def make_dirs(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def generate_random_models(num_models):
    for i in range(num_models):
        model_name = f"hops_random_model_{i+1}"  # define model name
        local_random_model_output_dir = os.path.join(
            LOCAL_OUTPUT_SIM_DIR, model_name
        )  # define local output dir name
        make_dirs(local_random_model_output_dir)  # make that dir

        # generate random model and save in local output dir
        user_params_file = os.path.join(LOCAL_BASE_PATH, "user_input_hops_k4.yml")
        tpl_file, est_file = generate_random_model.generate_model(user_params_file)

        # move files into the local output dir
        execute_command(["mv", tpl_file, est_file, local_random_model_output_dir])


def make_remote_output_dir():
    make_output_dir_cmd = ["mkdir " + REMOTE_FSC_OUTPUT_DIR]
    out_string, error_string = cluster_commands.send_cmd_to_cluster(
        ME_AT_REMOTE_URL, REMTOE_BASH_PROFILE_PATH, make_output_dir_cmd, LOCAL_OUT_DIR
    )


def copy_models_dir_to_cluster():
    copy_models_dir_to_cluster_cmd = [
        "scp",
        "-r",
        LOCAL_OUTPUT_SIM_DIR,
        ME_AT_REMOTE_URL + ":" + REMOTE_RESULTS_OUTPUT_DIR,
    ]
    out_string, error_string = cluster_commands.run_and_wait_on_process(
        copy_models_dir_to_cluster_cmd, LOCAL_OUT_DIR
    )


def create_job_scripts(num_models, num_sims_per_model):
    cluster_cmds = []
    partitions = ["epyc", "intel", "batch"]
    partition_counter = 0 # initialize the couter to 0
    max_jobs_per_array = 2499
    total_jobs_to_run = num_models * num_sims_per_model

    # step 1: figure out how many outer scripts there are
    num_outer_job_scripts = (
        total_jobs_to_run + max_jobs_per_array - 1
    ) // max_jobs_per_array

    index = 0

    for job in range(num_outer_job_scripts):
        job_name = f"hops_run_{job + 1}"
        partition = partitions[partition_counter]
        if partition_counter == len(partitions) - 1:
            partition_counter = 0
        else:
            partition_counter += 1

        # step 1a: make the params.txt file
        param_txt_file_base_name = f"params_{job + 1}.txt"
        param_txt_file_path = os.path.join(
            LOCAL_OUTPUT_COMMANDS_DIR, param_txt_file_base_name
        )
        params = []
        while len(params) < max_jobs_per_array and index < total_jobs_to_run:
            cur_model = index // num_sims_per_model
            cur_run = index % num_sims_per_model

            cur_random_model_dir = os.path.join(
                REMOTE_FSC_OUTPUT_DIR, f"hops_random_model_{cur_model + 1}"
            )
            params.append(
                [cur_random_model_dir, REMOTE_PROJECT_PATH, "hops", str(cur_run + 1)]
            )
            index += 1

        with open(param_txt_file_path, "w") as f:
            for param_line in params:
                line = " ".join(param_line)
                f.write(line + "\n")
        
        # step 1b: make individual scripts
        replacements = [
            ("JOB_NAME", job_name),
            ("PARTITION", partition),
            ("PARAM_FILE", param_txt_file_base_name),
            ("ARRAY_MAX", str(max_jobs_per_array)),
        ]
        job_script_name = job_name + ".sh"
        job = cluster_commands.write_sh_file(
            LOCAL_TEMPLATE_SLURM_FILE,
            LOCAL_OUTPUT_COMMANDS_DIR,
            job_script_name,
            replacements,
        )
        cluster_cmds.append(job_script_name)
    return cluster_cmds


def write_cluster_cmds_to_txt_file(cluster_cmds):
    with open(LOCAL_CLUSTER_CMDS_FILE, "w") as f:
        f.write("\n".join(cluster_cmds))
        f.write("\n")


"""SCRIPT"""
def run():
    num_models = 1000  # TODO: change to 1000
    num_sims_per_model = 100  # TODO: change to 100

    # make local output dirs
    make_dirs(LOCAL_OUT_DIR)
    make_dirs(LOCAL_OUTPUT_SIM_DIR)
    make_dirs(LOCAL_OUTPUT_COMMANDS_DIR)

    # step 1: generate random models
    # generate_random_models(num_models)
    print(" ************** MODELS GENERATED **************")

    # step 2: make remote output dirs (if not already made)
    # make_remote_output_dir()
    print(" ************** REMOTE DIRS MADE **************")

    # step 3: copy all output dirs to cluster
    # copy_models_dir_to_cluster()
    print(" ************** MODELS COPIED TO CLUSTER **************")

    # step 4: make scripts
    cluster_cmds = create_job_scripts(num_models, num_sims_per_model)
    write_cluster_cmds_to_txt_file(cluster_cmds)
    print(" ************** SCRIPTS GENERATED **************")

    # step 5: copy the submit all script to local output dir
    copy_script_cmd = ["cp", LOCAL_SUBMIT_JOBS_SCRIPT, LOCAL_OUTPUT_COMMANDS_DIR]
    execute_command(copy_script_cmd)

    # step 6: copy slurm cmds to remote dir
    copy_cluster_cmds_to_remote_cmd = [
        "scp",
        "-r",
        LOCAL_OUTPUT_COMMANDS_DIR,
        ME_AT_REMOTE_URL + ":" + REMOTE_SLURM_DESTINATION_DIR,
    ]
    # out_string, error_string = cluster_commands.run_and_wait_on_process(
    #     copy_cluster_cmds_to_remote_cmd, LOCAL_OUT_DIR
    # )
    print(" ************** SLURM CMDS COPIED **************")

    # step 7: submit jobs to remote
    """
    go to remote, navigate to the folder where the scripts are, and submit via terminal:
        `bash submit_all_slurm_jobs.sh cluster_cmds.txt > bash_output.txt`
    """
    return


run()
