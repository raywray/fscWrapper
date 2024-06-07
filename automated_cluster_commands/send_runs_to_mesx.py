import os
import subprocess
import time
import sys

import log

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utilities import generate_random_model


def make_output_dir(output_dir_path):
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)


def add_params_to_run_template():
    # initialize base paths
    mesx_base_path = "/home/resplin5072"
    # are we running this on raya's mac or lab comp?
    isMacBook = False
    if isMacBook:
        local_base_path = "/Users/raya/Documents/School/fscWrapper/"
    else:
        local_base_path = "/home/raya/Documents/Projects/fscWrapper/"

    # initialize constant vars
    mesx_project_path = os.path.join(mesx_base_path, "fscWrapper")
    simulation_subfolder = "fsc_output"
    me_at_remote_URL = "resplin5072@mesx.sdsu.edu"
    local_template_sh_file = os.path.join(
        local_base_path, "automated_cluster_commands/qsub-template.sh"
    )
    local_out_dir = os.path.join(local_base_path, "sim_output")
    mesx_cluster_cmds_folder = os.path.join(mesx_base_path, "cluster_commands")
    mesx_out_dir = os.path.join("/usr/scratch2/userdata2/resplin5072", "output")
    mesx_qsub_script_destination_folder = os.path.join(
        mesx_cluster_cmds_folder, simulation_subfolder
    )
    mesx_fsc_output_dir = os.path.join(mesx_out_dir, simulation_subfolder)
    local_output_simulation_dir = os.path.join(local_out_dir, simulation_subfolder)
    local_output_cmds_folder = os.path.join(local_out_dir, "qsub_commands")
    local_initial_submit_jobs_script_path = os.path.join(
        local_base_path, "automated_cluster_commands/submit_all_jobs.sh"
    )
    local_cluster_cmds_txt_file_path = os.path.join(
        local_output_cmds_folder, "cluster_cmds.txt"
    )

    # make local output dirs
    make_output_dir(local_out_dir)
    make_output_dir(local_output_simulation_dir)
    make_output_dir(local_output_cmds_folder)

    # *********END OF SETUP********************************************************
    # *********START OF SCRIPT*****************************************************

    # step 1: define number of randomly generated models
    num_models = 1000  # TODO: change to 1000
    num_simulations_per_model = 1000  # TODO: change to 1000

    # step 2: generate random models
    generate_random_models(num_models, local_output_simulation_dir, local_base_path)

    # now I need to copy all those new output_dirs to mesx
    # first, make mesx output dir
    make_mesx_output_dir(mesx_fsc_output_dir, me_at_remote_URL, local_out_dir)
    # now, copy all the output dirs to mesx
    copy_model_dirs_to_mesx(
        local_output_simulation_dir, me_at_remote_URL, mesx_out_dir, local_out_dir
    )

    # now, create all the .sh files
    cluster_cmds = create_job_scripts(
        num_models,
        num_simulations_per_model,
        mesx_fsc_output_dir,
        mesx_project_path,
        local_template_sh_file,
        local_output_cmds_folder,
    )

    # write cluster cmds to txt file
    write_cluster_cmds_to_txt_file(cluster_cmds, local_cluster_cmds_txt_file_path)

    # copy submit all jobs to local out dir
    os.system(f"cp {local_initial_submit_jobs_script_path} {local_output_cmds_folder}")

    # copy over folder cluster cmds
    copy_cluster_cmds_to_mesx(
        local_output_cmds_folder,
        me_at_remote_URL,
        mesx_qsub_script_destination_folder,
        local_out_dir,
    )

    # submit job to mesx
    submit_full_jobs_to_mesx(
        mesx_qsub_script_destination_folder, me_at_remote_URL, local_out_dir
    )


def write_cluster_cmds_to_txt_file(cluster_cmds, local_cluster_cmds_txt_file_path):
    with open(local_cluster_cmds_txt_file_path, "w") as f:
        f.write("\n".join(cluster_cmds))
        f.write("\n")


def submit_full_jobs_to_mesx(
    mesx_qsub_script_destination_folder, me_at_remote_URL, local_out_dir
):
    full_sumbit_job_mesx_cmd = [
        "cd " + mesx_qsub_script_destination_folder + ";",
        "bash submit_all_jobs.sh cluster_cmds.txt;",
    ]
    out_string, error_string = send_cmd_to_cluster(
        me_at_remote_URL, full_sumbit_job_mesx_cmd, local_out_dir, retry=True
    )


def make_mesx_output_dir(mesx_fsc_output_dir, me_at_remote_URL, local_out_dir):
    make_output_dir_cmd = ["mkdir " + mesx_fsc_output_dir]
    out_string, error_string = send_cmd_to_cluster(
        me_at_remote_URL, make_output_dir_cmd, local_out_dir
    )


def copy_cluster_cmds_to_mesx(
    local_output_cmds_folder,
    me_at_remote_URL,
    mesx_qsub_script_destination_folder,
    local_out_dir,
):
    copy_cluster_cmds_to_mesx_cmd = [
        "scp",
        "-r",
        local_output_cmds_folder,
        me_at_remote_URL + ":" + mesx_qsub_script_destination_folder,
    ]
    print(" ".join(copy_cluster_cmds_to_mesx_cmd))
    out_string, error_string = run_and_wait_on_process(
        copy_cluster_cmds_to_mesx_cmd, local_out_dir
    )


def copy_model_dirs_to_mesx(
    local_output_simulation_dir, me_at_remote_URL, mesx_out_dir, local_out_dir
):
    copy_model_output_dirs_to_mesx_cmd = [
        "scp",
        "-r",
        local_output_simulation_dir,
        me_at_remote_URL + ":" + mesx_out_dir,
    ]
    print(" ".join(copy_model_output_dirs_to_mesx_cmd))
    out_string, error_string = run_and_wait_on_process(
        copy_model_output_dirs_to_mesx_cmd, local_out_dir
    )
    print("copied all files to mesx")


def generate_random_models(num_models, local_output_simulation_dir, local_base_path):
    for i in range(num_models):
        model_name = f"hops_random_model_{i+1}"
        # define the output dir name
        local_random_model_output_dir = os.path.join(
            local_output_simulation_dir, model_name
        )
        make_output_dir(local_random_model_output_dir)
        # generate random model and save in local output dir
        user_parms_yml = f"{local_base_path}/user_input_hops_k4.yml"

        tpl_file, est_file = generate_random_model.generate_model(user_parms_yml)

        # move files into the local output dir
        os.system(f"mv {tpl_file} {local_random_model_output_dir}")
        os.system(f"mv {est_file} {local_random_model_output_dir}")


def create_job_scripts(
    num_models,
    num_simulations_per_model,
    mesx_fsc_output_dir,
    mesx_project_path,
    local_template_sh_file,
    local_output_cmds_folder,
):
    cluster_cmds = []

    for i in range(num_models):
        for j in range(num_simulations_per_model):
            job_name = f"hops_run_{i+1}:{j+1}"
            new_script_file_name = job_name + ".sh"

            cur_mesx_model_output_dir_name = os.path.join(
                mesx_fsc_output_dir, f"hops_random_model_{i+1}"
            )
            sh_replacements = [
                ("JOBNAME", job_name),
                ("OUTPUT_DIR", cur_mesx_model_output_dir_name),
                ("PROJECT_PATH", mesx_project_path),
                ("PREFIX", "hops"),
                ("CUR_RUN", str(j + 1)),
            ]
            new_sh_created = write_sh_file(
                local_template_sh_file,
                local_output_cmds_folder,
                new_script_file_name,
                sh_replacements,
            )
            cluster_cmds.append(new_script_file_name)
    return cluster_cmds


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


def run_and_wait_on_process(cmd, folder):
    program = cmd[0]
    log.write_to_log(" ".join(cmd))
    process_completed_result = subprocess.run(cmd, capture_output=True, cwd=folder)
    error_string = process_completed_result.stderr.decode()
    out_string = process_completed_result.stdout.decode()

    colored_error_string = "\033[93m" + "ERROR:  " + error_string + "\x1b[0m"

    if len(error_string) > 0:
        log.write_to_log(colored_error_string)

    with open(os.path.join(folder, program + "_stderr.txt"), "w") as f:
        f.writelines(error_string)
    with open(os.path.join(folder, program + "_stdout.txt"), "w") as f:
        f.writelines(out_string)

    return out_string, error_string


def run_and_wait_with_retry(cmd, folder, excuse, num_retries_allowed, sleepy_time):
    num_tries = 0

    while True:
        out_string, error_string = run_and_wait_on_process(cmd, folder)
        num_tries = num_tries + 1
        if num_tries > num_retries_allowed:
            break

        if excuse in error_string:
            log.write_to_log(
                "Got " + excuse + ". Retrying " + str(num_tries) + " time."
            )
            log.write_to_log("Wait for " + str(sleepy_time) + " secs.")
            time.sleep(sleepy_time)
        else:
            break
    return out_string, error_string


def send_cmd_to_cluster(
    remote_url,
    cmd_list,
    out_dir,
    excuse="Connection reset by peer",
    num_re_all=3,
    sleepy_time=10,
    retry=False,
):
    cmds_to_append = ["ssh", remote_url, ". /home/resplin5072/.bash_profile;"]
    cmds_to_send = cmds_to_append + cmd_list
    print(" ".join(cmds_to_send))
    if retry:
        out_string, error_string = run_and_wait_with_retry(
            cmds_to_send, out_dir, excuse, num_re_all, sleepy_time
        )
    else:
        out_string, error_string = run_and_wait_on_process(cmds_to_send, out_dir)
    return out_string, error_string


# run command
add_params_to_run_template()
