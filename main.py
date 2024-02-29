from pipeline_modules import generate_random_tpl, generate_random_est

tpl_filename = "random.tpl"
est_filename = "random.est"

generate_random_tpl.random_initializations(tpl_filename)
generate_random_est.create_est(tpl_filename, est_filename)
