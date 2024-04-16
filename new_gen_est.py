def write_est(simple_params, complex_params, est_filename):
    lines = (
        [
            "// Priors and rules file",
            "// *********************",
            "",
            "[PARAMETERS]",
            "//#isInt? #name #dist. #min #max",
        ]
        + [param for param in simple_params]
        + [
            "",
            "[COMPLEX PARAMETERS]",
            "",
        ]
        + [param for param in complex_params]
    )

    # write to file
    with open(est_filename, "w") as file:
        for line in lines:
            file.write(line + "\n")

def get_mutation_rate_params(mutation_rate_dist):
    return "0 MUTRATE {} {} {} output".format(
        mutation_rate_dist["type"],
        mutation_rate_dist["min"],
        mutation_rate_dist["max"],
    )

def get_simple_params(mutation_rate_dist):
    simple_params = []
    # get mutation rate params
    simple_params.append(get_mutation_rate_params(mutation_rate_dist))

    # effective size params

    return simple_params

def get_complex_params():
    return []

def create_est(mutation_rate_dist):
    simple_params = get_simple_params(mutation_rate_dist)
    complex_params = get_complex_params()

    write_est(simple_params, complex_params, "est_test.est")

mutation_rate_dist = {"min": 1e-7, "max": 1e-9, "type": "unif"}
create_est(mutation_rate_dist=mutation_rate_dist)

