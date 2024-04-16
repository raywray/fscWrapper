import re

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


def get_params_from_tpl(tpl, search_params):
    return [line for line in tpl if search_params in line]


def get_mutation_rate_params(mutation_rate_dist):
    return [
        "0 MUTRATE {} {} {} output".format(
            mutation_rate_dist["type"],
            mutation_rate_dist["min"],
            mutation_rate_dist["max"],
        )
    ]


def get_effective_size_params(tpl, ne_dist):
    # parse tpl
    effective_size_params_from_tpl = get_params_from_tpl(tpl, search_params="NPOP_")
    effective_size_params = [
        "1 {} {} {} {} output".format(
            param, ne_dist["type"], ne_dist["min"], ne_dist["max"]
        )
        for param in effective_size_params_from_tpl
    ]
    # set values
    return effective_size_params


def get_migration_params(tpl, mig_dist):
    migration_params = []
    mig_params_from_tpl = get_params_from_tpl(tpl, "MIG")
    migration_pattern = r"\bMIG\w*"
    unique_params = set()

    for loc in mig_params_from_tpl:
        unique_params.update(re.findall(migration_pattern, loc))
    migration_params = [
        "0 {} {} {} {} output".format(
            param, mig_dist["type"], mig_dist["min"], mig_dist["max"]
        )
        for param in list(unique_params)
    ]
    return migration_params


def get_simple_params(tpl, mutation_rate_dist, ne_dist, mig_dist):
    simple_params = []
    # get mutation rate params
    simple_params.extend(get_mutation_rate_params(mutation_rate_dist))

    # effective size params
    simple_params.extend(get_effective_size_params(tpl, ne_dist))

    # get migration params
    simple_params.extend(get_migration_params(tpl, mig_dist))
    return simple_params


def get_complex_params():
    return []


def create_est(tpl_filepath, mutation_rate_dist, ne_dist, mig_dist):
    # convert tpl file to list
    tpl = []
    with open(tpl_filepath, "r") as tpl_file:
        for line in tpl_file:
            tpl.append(line.strip())

    # get simple params
    simple_params = get_simple_params(
        tpl=tpl,
        mutation_rate_dist=mutation_rate_dist,
        ne_dist=ne_dist,
        mig_dist=mig_dist,
    )

    # get complex params
    complex_params = get_complex_params()

    write_est(simple_params, complex_params, "est_test.est")


tpl_filepath = "tpl_test.tpl"
ne_dist = {"min": 1e-7, "max": 1e-9, "type": "unif"}
mutation_rate_dist = {"min": 1e-7, "max": 1e-9, "type": "unif"}
mig_dist = {"min": 1e-7, "max": 1e-9, "type": "unif"}
create_est(
    tpl_filepath=tpl_filepath,
    mutation_rate_dist=mutation_rate_dist,
    ne_dist=ne_dist,
    mig_dist=mig_dist,
)
