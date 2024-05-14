import os
import subprocess
import time

import log

def execute_command(command):
    os.system(command)


def add_params_to_run_template():
    project_path = "/home/resplin5072/fscWrapper/"
    simulation_subfolder = "fsc_output"
    me_at_remote_URL = "resplin5072@mesx.sdsu.edu"
    template_sh_file = "/home/raya/Documents/Projects/fscWrapper/automated_cluster_commands/qsub-template.sh"
    local_out_dir = "/home/raya/Documents/Projects/fscWrapper/sim_output"
    commands_folder_mesx = "/home/resplin5072/cluster_commands"
    out_folder_on_mesx = "/home/resplin5072/output"
    script_destination_folder_mesx = os.path.join(
        commands_folder_mesx, simulation_subfolder
    )
    fsc_output_path_mesx = os.path.join(out_folder_on_mesx, simulation_subfolder)
    origin_folder = os.path.join(local_out_dir, simulation_subfolder)

    cluster_cmds = []

    if not os.path.exists(local_out_dir):
        os.makedirs(local_out_dir)
    if not os.path.exists(origin_folder):
        os.makedirs(origin_folder)

    number_of_sims = 1000 # TODO: hardcoded

    for i in range(number_of_sims):
        job_name = f"hops_run_{i+1}"

        new_script_file_name = job_name + ".sh"
        output_dir_name = fsc_output_path_mesx + "/" + job_name + "_output"
        sh_replacements = [("JOBNAME", job_name), ("OUTPUT_DIR", output_dir_name), ("PROJECT_PATH", project_path)]

        new_sh_created = write_sh_file(
            template_sh_file, origin_folder, new_script_file_name, sh_replacements
        )
        cluster_cmds.append(new_script_file_name)

    # copy over the folder of cluster commands
    copy_cluster_cmds = [
        "scp", "-r", origin_folder, me_at_remote_URL + ":" + commands_folder_mesx
    ]
    print(" ".join(copy_cluster_cmds))
    out_string, error_string = run_and_wait_on_process(copy_cluster_cmds, local_out_dir)

    # make output dir 
    make_out_dir_cmd = [
        "mkdir " + fsc_output_path_mesx
    ]
    out_string, error_string = send_cmd_to_cluster(me_at_remote_URL, make_out_dir_cmd, local_out_dir)

    cmds_to_qsub_via_ssh = []
    for cmd in cluster_cmds:
        cmds_to_qsub_via_ssh.append("qsub")
        cmds_to_qsub_via_ssh.append(cmd + ";")

    # submit all qsub commands
    full_cmd_with_all_qsubs = [
        "cd " + script_destination_folder_mesx + ";",
    ] + cmds_to_qsub_via_ssh
    out_string, error_string = send_cmd_to_cluster(me_at_remote_URL, full_cmd_with_all_qsubs, local_out_dir, retry=True)
    
    return


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

def send_cmd_to_cluster(remote_url,cmd_list, out_dir, excuse="Connection reset by peer", num_re_all=3, sleepy_time=10, retry=False):
    cmds_to_append = ["ssh", remote_url, ". /home/resplin5072/.bash_profile;"]
    cmds_to_send = cmds_to_append + cmd_list
    print(" ".join(cmds_to_send))
    if retry:
        out_string, error_string = run_and_wait_with_retry(cmds_to_send, out_dir, excuse, num_re_all, sleepy_time)
    else:
        out_string, error_string = run_and_wait_on_process(cmds_to_send, out_dir)
    return out_string, error_string

add_params_to_run_template()