import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utilities import generate_random_model, cluster_commands


def make_output_dir(output_dir_path):
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)


def add_params_to_run_template():
    # initialize base paths
    mesx_base_path = "/home/resplin5072"
    mesx_output_base_path = "/usr/scratch2/userdata2/resplin5072"
    # are we running this on raya's mac or lab comp?
    isMacBook = False
    if isMacBook:
        local_base_path = "/Users/raya/Documents/School/fscWrapper/"
    else:
        local_base_path = "/home/raya/Documents/Projects/fscWrapper/"

    # initialize constant vars
    mesx_bash_profile_path = os.path.join(mesx_base_path, ".bash_profile")
    mesx_project_path = os.path.join(mesx_base_path, "fscWrapper")
    simulation_subfolder = "fsc_output"
    me_at_remote_URL = "resplin5072@mesx.sdsu.edu"
    local_template_sh_file = os.path.join(
        local_base_path, "automated_cluster_commands/qsub-template-2.sh"
    )
    local_out_dir = os.path.join(local_base_path, "sim_output")
    # mesx_cluster_cmds_folder = os.path.join(mesx_base_path, "cluster_commands")
    mesx_cluster_cmds_folder = os.path.join(mesx_output_base_path, "cluster_commands")
    mesx_out_dir = os.path.join(mesx_output_base_path, "output")
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
    num_simulations_per_model = 100  # TODO: change to 100

    # step 2: generate random models
    # generate_random_models(num_models, local_output_simulation_dir, local_base_path)

    # make mesx output dir
    # make_mesx_output_dir(mesx_fsc_output_dir, mesx_bash_profile_path, me_at_remote_URL, local_out_dir)

    # copy all the output dirs to mesx
    # copy_model_dirs_to_mesx(
    #     local_output_simulation_dir, me_at_remote_URL, mesx_out_dir, local_out_dir
    # )

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
    # submit_full_jobs_to_mesx(
    #     mesx_qsub_script_destination_folder, mesx_bash_profile_path, me_at_remote_URL, local_out_dir
    # )


def write_cluster_cmds_to_txt_file(cluster_cmds, local_cluster_cmds_txt_file_path):
    with open(local_cluster_cmds_txt_file_path, "w") as f:
        f.write("\n".join(cluster_cmds))
        f.write("\n")


def submit_full_jobs_to_mesx(
    mesx_qsub_script_destination_folder, me_at_remote_URL, bash_profile_path, local_out_dir
):
    full_sumbit_job_mesx_cmd = [
        "cd " + mesx_qsub_script_destination_folder + ";",
        "bash submit_all_jobs.sh cluster_cmds.txt;",
    ]
    out_string, error_string = cluster_commands.send_cmd_to_cluster(
        me_at_remote_URL, bash_profile_path, full_sumbit_job_mesx_cmd, local_out_dir, retry=True
    )


def make_mesx_output_dir(mesx_fsc_output_dir, me_at_remote_URL, bash_profile_path, local_out_dir):
    make_output_dir_cmd = ["mkdir " + mesx_fsc_output_dir]
    out_string, error_string = cluster_commands.send_cmd_to_cluster(
        me_at_remote_URL, bash_profile_path, make_output_dir_cmd, local_out_dir
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
    out_string, error_string = cluster_commands.run_and_wait_on_process(
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
    out_string, error_string = cluster_commands.run_and_wait_on_process(
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

    for i in range(2, num_models + 1):
        node_option_20 = "nodes=1:ppn=20:priority1"
        node_option_4 = "nodes=1:ppn=4:priority1"
        node_option_56 = "nodes=1:ppn=56:priority2"
        cur_mesx_model_output_dir_name = os.path.join(
            mesx_fsc_output_dir, f"hops_random_model_{i}"
        )
        sh_replacements = [
            ("OUTPUT_DIR", cur_mesx_model_output_dir_name),
            ("PROJECT_PATH", mesx_project_path),
            ("PREFIX", "hops"),
        ]

        # send 56 jobs, then 20, then 20, then 4
        job_name = f"hops_run_{i}:1-56"
        batch_1_script_file_name = job_name + ".sh"
        batch_1_replacements = sh_replacements + [
            ("NODES", node_option_56),
            ("NUM_FIRST_SIM", "1"),
            ("NUM_LAST_SIM", "56"),
            ("JOBNAME", job_name),
        ]

        batch_1 = write_sh_file(
            local_template_sh_file,
            local_output_cmds_folder,
            batch_1_script_file_name,
            batch_1_replacements
        )
        cluster_cmds.append(batch_1_script_file_name)

        # send next 20
        job_name = f"hops_run_{i}:57-76"
        batch_2_script_file_name = job_name + ".sh"
        batch_2_replacements = sh_replacements + [
            ("NODES", node_option_20),
            ("NUM_FIRST_SIM", "57"),
            ("NUM_LAST_SIM", "76"),
            ("JOBNAME", job_name),
        ]

        batch_2 = write_sh_file(
            local_template_sh_file,
            local_output_cmds_folder,
            batch_2_script_file_name,
            batch_2_replacements
        )
        cluster_cmds.append(batch_2_script_file_name)

        # send another 20
        job_name = f"hops_run_{i}:77-96"
        batch_3_script_file_name = job_name + ".sh"
        batch_3_replacements = sh_replacements + [
            ("NODES", node_option_20),
            ("NUM_FIRST_SIM", "77"),
            ("NUM_LAST_SIM", "96"),
            ("JOBNAME", job_name),
        ]

        batch_3 = write_sh_file(
            local_template_sh_file,
            local_output_cmds_folder,
            batch_3_script_file_name,
            batch_3_replacements
        )
        cluster_cmds.append(batch_3_script_file_name)

        # send last 4
        job_name = f"hops_run_{i}:97-100"
        batch_4_script_file_name = job_name + ".sh"
        batch_4_replacements = sh_replacements + [
            ("NODES", node_option_4),
            ("NUM_FIRST_SIM", "97"),
            ("NUM_LAST_SIM", "100"),
            ("JOBNAME", job_name),
        ]

        batch_4 = write_sh_file(
            local_template_sh_file,
            local_output_cmds_folder,
            batch_4_script_file_name,
            batch_4_replacements
        )
        cluster_cmds.append(batch_4_script_file_name)

    # this is old code 
    # for i in range(num_models):
    #     for j in range(num_simulations_per_model):
    #         job_name = f"hops_run_{i+1}:{j+1}"
    #         new_script_file_name = job_name + ".sh"

    #         cur_mesx_model_output_dir_name = os.path.join(
    #             mesx_fsc_output_dir, f"hops_random_model_{i+1}"
    #         )

    #         sh_replacements = [
    #             ("JOBNAME", job_name),
    #             ("OUTPUT_DIR", cur_mesx_model_output_dir_name),
    #             ("PROJECT_PATH", mesx_project_path),
    #             ("PREFIX", "hops"),
    #             ("CUR_RUN", str(j + 1)),
    #         ]
    #         new_sh_created = write_sh_file(
    #             local_template_sh_file,
    #             local_output_cmds_folder,
    #             new_script_file_name,
    #             sh_replacements,
    #         )
    #         cluster_cmds.append(new_script_file_name)
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

# run command
add_params_to_run_template()
