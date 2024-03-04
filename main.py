from pipeline_modules import generate_random_tpl, generate_random_est

# User Provided Input
MUTATION_RATE_MIN = 1e-7
MUTATION_RATE_MAX = 1e-9
NUM_POPS = 3
SAMPLE_SIZES = [2, 4, 4]

tpl_filename = "test2.tpl"
est_filename = "test2.est"

generate_random_tpl.generate_random_tpl_parameters(tpl_filename, NUM_POPS, SAMPLE_SIZES)
generate_random_est.create_est(tpl_filename, est_filename, mutrate_min=MUTATION_RATE_MIN, mutrate_max=MUTATION_RATE_MAX)

# command to run fsc
# fsc27093 -t LD-pruned_SNPs.tpl -e LD-pruned_SNPs.est -m -n 10000 -L 50 -s 0 -M
