from pipeline_modules import generate_random_tpl, generate_random_est

tpl_filename = "random.tpl"
est_filename = "random.est"

generate_random_tpl.generate_random_tpl_parameters(tpl_filename)
generate_random_est.create_est(tpl_filename, est_filename)

# command to run fsc
# fsc27093 -t LD-pruned_SNPs.tpl -e LD-pruned_SNPs.est -m -n 10000 -L 50 -s 0 -M
