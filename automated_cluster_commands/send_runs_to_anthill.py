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
LOCAL_TEMPLATE_SH_FILE = os.path.join(
    LOCAL_BASE_PATH, "automated_cluster_commands", "anthill_job_template.sh"
)
LOCAL_OUT_DIR = os.path.join(LOCAL_BASE_PATH, "sim_output")
LOCAL_OUTPUT_SIM_DIR = os.path.join(LOCAL_OUT_DIR, SIMULATION_SUB_FOLDER)
LOCAL_OUTPUT_COMMANDS_DIR = os.path.join(LOCAL_OUT_DIR, "script_commands")
LOCAL_CLUSTER_CMDS_FILE = os.path.join(LOCAL_OUTPUT_COMMANDS_DIR, "cluster_cmds.txt")
LOCAL_SUBMIT_JOBS_SCRIPT = os.path.join(
    LOCAL_BASE_PATH, "automated_cluster_commands", "submit_anthill_jobs.sh"
)

# remote
REMOTE_BASE_PATH = "/home3/resplin5072"
REMTOE_BASH_PROFILE_PATH = os.path.join(REMOTE_BASE_PATH, ".bash_profile")
REMOTE_OUTPUT_BASE_PATH = "/usr/scratchF/resplin5072"
REMOTE_PROJECT_PATH = os.path.join(REMOTE_BASE_PATH, "Projects", "fscWrapper")
ME_AT_REMOTE_URL = "resplin5072@anthill.sdsu.edu"
REMOTE_CLUSTER_CMDS_DIR = os.path.join(REMOTE_OUTPUT_BASE_PATH, "cluster_commands")
REMOTE_RESULTS_OUTPUT_DIR = os.path.join(REMOTE_OUTPUT_BASE_PATH, "output")
REMOTE_SCRIPT_DESTINATION_DIR = os.path.join(
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


def make_remote_output_dir():
    make_output_dir_cmd = ["mkdir " + REMOTE_FSC_OUTPUT_DIR]
    out_string, error_string = cluster_commands.send_cmd_to_cluster(
        ME_AT_REMOTE_URL, REMTOE_BASH_PROFILE_PATH, make_output_dir_cmd, LOCAL_OUT_DIR
    )


def make_scripts(model_start_number, num_sims, num_models_to_submit_at_a_time):
    cluster_commands = []
    node_option_1 = "nodes=1:ppn=16:priority1"
    node_option_2 = "nodes=1:ppn=4:priority1"

    def populate_batch(node_option, first, last, jobname, sh_replacements):
        batch_script_name = job_name + ".sh"

        replacements = sh_replacements + [
            ("NODES", node_option),
            ("NUM_FIRST_SIM", str(first)),
            ("NUM_LAST_SIM", str(last)),
            ("JOBNAME", jobname),
        ]
        batch = write_sh_file(
            LOCAL_TEMPLATE_SH_FILE,
            LOCAL_OUTPUT_COMMANDS_DIR,
            batch_script_name,
            replacements,
        )

        cluster_commands.append(batch_script_name)

    for i in range(model_start_number, model_start_number - num_models_to_submit_at_a_time, -1):
        cur_model_out_dir_name = os.path.join(
            REMOTE_FSC_OUTPUT_DIR, f"hops_random_model_{i}"
        )

        sh_replacements = [
            ("OUTPUT_DIR", cur_model_out_dir_name),
            ("PROJECT_PATH", REMOTE_PROJECT_PATH),
            ("PREFIX", "hops"),
        ]

        for j in range(1, num_sims, 16):
            start = j
            if j + 15 > num_sims:
                end = num_sims
            else:
                end = j + 15
            job_name = f"hops_run_{i}:{start}-{end}"
            node_option = node_option_1 if end % 16 == 0 else node_option_2
            populate_batch(node_option, start, end, job_name, sh_replacements)

    return cluster_commands


def write_cluster_cmds_to_txt_file(cluster_cmds):
    with open(LOCAL_CLUSTER_CMDS_FILE, "w") as f:
        f.write("\n".join(cluster_cmds))
        f.write("\n")


def write_sh_file(template_file, out_dir, new_file_name, replacements):
    lines_to_write = []
    new_sh_file = os.path.join(out_dir, new_file_name)

    with open(template_file, "r") as f:
        while True:
            line = f.readline()
            new_line = line

            for r_tuple in replacements:
                out_with_the_old = r_tuple[0]
                in_with_the_new = r_tuple[1]

                if out_with_the_old in line:
                    new_line = line.replace(out_with_the_old, in_with_the_new)
            lines_to_write.append(new_line)
            if not line:
                break
    with open(new_sh_file, "w") as f:
        for line in lines_to_write:
            f.writelines(line)
    return new_sh_file


def copy_ucr_dirs_to_anthill(beginning_model_num, num_models_to_move):
    # copy to local, then copy to anthill
    ucr_models_out_dir_path = "/bigdata/armstronglab/respl001/output/fsc_output"
    copy_cmds = []

    def copy_ucr_to_machine():
        for i in range(beginning_model_num, beginning_model_num - num_models_to_move, -1):
            cmd = [
                "scp",
                "-r",
                f"respl001@cluster.hpcc.ucr.edu:{ucr_models_out_dir_path}/hops_random_model_{i}/",
                LOCAL_OUTPUT_SIM_DIR + ";",
            ]
            copy_cmds.append(" ".join(cmd))
            # out_string, error_string = cluster_commands.run_and_wait_on_process(cmd, LOCAL_OUT_DIR)
        execute_command(copy_cmds)
    
    copy_ucr_to_machine()
    cmd = [
        "scp",
        "-r",
        LOCAL_OUTPUT_SIM_DIR,
        ME_AT_REMOTE_URL + ":" + REMOTE_RESULTS_OUTPUT_DIR,
    ]
    out_string, error_string = cluster_commands.run_and_wait_on_process(
        cmd, LOCAL_OUT_DIR
    )


"""SCRIPT"""


def run():
    beginning_model_num = 896  # starts from the back, will do 5 models (need to manually change this to go down)
    num_sims_per_model = 100
    num_models_to_submit_at_a_time = 20 # it is 7 scripts per model

    # make local output dirs
    make_dirs(LOCAL_OUT_DIR)
    make_dirs(LOCAL_OUTPUT_SIM_DIR)
    make_dirs(LOCAL_OUTPUT_COMMANDS_DIR)

    # step 1: make remote out dirs
    # make_remote_output_dir() TODO: this is done in the copy dirs function
    print(" ************** REMOTE DIRS MADE **************")

    # step 2: move 100 models from ucr to anthill (start from the back)
    # copy_ucr_dirs_to_anthill(beginning_model_num, num_models_to_move) NOTE: DONEEEEEE
    print(" ************** MODELS MOVED ******************")

    # step 3: make scripts
    cluster_cmds = make_scripts(beginning_model_num, num_sims_per_model, num_models_to_submit_at_a_time)
    write_cluster_cmds_to_txt_file(cluster_cmds)
    print(" ************** SCRIPTS GENERATED **************")

    # step 4: copy submit all script to local out dir
    copy_script_cmd = [
        "cp",
        LOCAL_SUBMIT_JOBS_SCRIPT,
        LOCAL_OUTPUT_COMMANDS_DIR,
    ]
    execute_command(copy_script_cmd)

    # step 6: copy pbs scripts to remote dir
    copy_cluster_cmds_to_remote_cmd = [
        "scp",
        "-r",
        LOCAL_OUTPUT_COMMANDS_DIR,
        ME_AT_REMOTE_URL + ":" + REMOTE_SCRIPT_DESTINATION_DIR,
    ]
    out_string, error_string = cluster_commands.run_and_wait_on_process(
        copy_cluster_cmds_to_remote_cmd, LOCAL_OUT_DIR
    )
    print(" ************** SCRIPT CMDS COPIED **************")

    # step 7: submit jobs to remote
    """
    go to remote, navigate to the folder where the scripts are, and submit via terminal:
        `bash submit_anthill_jobs.sh cluster_cmds.txt > bash_output.txt`
    """


run()
