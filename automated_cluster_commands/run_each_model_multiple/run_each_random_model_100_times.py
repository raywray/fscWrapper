import os


def rename_to_random_models(base_output_dir):

    # Define the path to the output directory

    # Get a list of all subdirectories in the output directory
    batch_subdirs = [
        d
        for d in os.listdir(base_output_dir)
        if os.path.isdir(os.path.join(base_output_dir, d))
    ]
    # print(batch_subdirs)

    # step 1: enter each bath dir
    # step 2: rename each run dir to random model dir

    # Iterate over the subdirectories and rename them
    for i, batch in enumerate(batch_subdirs, start=1):
        batch_path = os.path.join(base_output_dir, batch)
        cur_subdirs = [
            d
            for d in os.listdir(batch_path)
            if os.path.isdir(os.path.join(batch_path, d))
        ]
        # print(cur_subdirs)
        for j, subdir in enumerate(cur_subdirs, start=1):
            model_number = subdir.split("_")[1]
            old_path = os.path.join(batch_path, subdir)
            new_subdir_name = f"random_model_{model_number}"
            new_path = os.path.join(batch_path, new_subdir_name)
            os.rename(old_path, new_path)
    return

# step 1: access each current batch (hops_run_1_output FOR EXAMPLE)
# step 2: rename the folders from run_1 to random_model_1
# step 3: go into each random model and run that model 100 times


base_output_dir = "/Users/raya/Documents/School/fscWrapper/output/fsc_output"
prefix = "hops"

# rename_to_random_models(base_output_dir)
