from pipeline_modules import generate_random_tpl, generate_random_est

# User Provided Input
NUM_POPS = 3
SAMPLE_SIZES = [2, 4, 4]
MUTATION_RATE_DIST = {"min": 1e-7, "max": 1e-9, "type": "unif"}
EFFECTIVE_POP_SIZE_DIST = {"min": 100, "max": 300000, "type": "unif"}
RESIZED_DIST = {"min": 0, "max": 100, "type": "unif"}
ADMIX_DIST = {"min": 0, "max": 0.25, "type": "unif"}
MIGRATION_DIST = {"type": "logunif", "min": 1e-10, "max": 1e-1}
TIME_DIST = {
    "type": "unif",
    "single_max": 5000,
    "single_min": 1,
    "multiple_max": 600,
    "multiple_min": 1,
    "extra_max": 500,
    "extra_min": 0,
}

# Define file names
tpl_filename = "testing_again.tpl"
est_filename = "testing_again.est"

# Generate random tpl and est files
generate_random_tpl.generate_random_tpl_parameters(tpl_filename, NUM_POPS, SAMPLE_SIZES)
generate_random_est.create_est(
    tpl_filename,
    est_filename,
    mutation_rate_dist=MUTATION_RATE_DIST,
    ne_dist=EFFECTIVE_POP_SIZE_DIST,
    resized_dist=RESIZED_DIST,
    admix_dist=ADMIX_DIST,
    time_dist=TIME_DIST,
    mig_dist=MIGRATION_DIST
)

# command to run fsc
# fsc27093 -t LD-pruned_SNPs.tpl -e LD-pruned_SNPs.est -m -n 10000 -L 50 -s 0 -M
