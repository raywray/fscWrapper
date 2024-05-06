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


def get_effective_size_params(tpl, effective_pop_size_dist):
    # parse tpl
    effective_size_params_from_tpl = get_params_from_tpl(tpl, search_params="NPOP_")
    effective_size_params = [
        "1 {} {} {} {} output".format(
            param,
            effective_pop_size_dist["type"],
            effective_pop_size_dist["min"],
            effective_pop_size_dist["max"],
        )
        for param in effective_size_params_from_tpl
    ]
    # set values
    return effective_size_params


def find_unique_params(list_to_search, pattern_to_find):
    unique_params = set()
    for element in list_to_search:
        unique_params.update(re.findall(pattern_to_find, element))
    return list(unique_params)


def get_migration_params(tpl, migration_dist):
    mig_params_from_tpl = get_params_from_tpl(tpl, "MIG")
    migration_pattern = r"\bMIG\w*"

    unique_migration_params = find_unique_params(mig_params_from_tpl, migration_pattern)
    migration_params = [
        "0 {} {} {} {} output".format(
            param, migration_dist["type"], migration_dist["min"], migration_dist["max"]
        )
        for param in unique_migration_params
    ]
    return migration_params


def get_divergence_event_params(divergence_params, time_dist):
    simple_div_params = []
    complex_div_params = []
    space_between_events_min = 0
    space_between_events_max = (
        1000  # NOTE: OG stephanie code was 500. HARDCODED, can change
    )

    # define some functions
    def add_event_to_param(time_parameters, event, min, max):
        time_parameters.append(
            "1 {} {} {} {} output".format(
                event,
                time_dist["type"],
                min,
                max,
            )
        )

    def add_first_div_event_to_simple_params():
        add_event_to_param(
            simple_div_params,
            divergence_params[0],
            time_dist["min"],
            time_dist["max"],
        )

    # decide whether time or complex param
    if len(divergence_params) == 1:
        # only one, add to simple
        add_first_div_event_to_simple_params()

    elif len(divergence_params) > 1:
        # there are more -- add the first to simple, rest to complex
        # NOTE: in OG stephanie code, the min was 1 and max 600
        add_first_div_event_to_simple_params()

        for i in range(1, len(divergence_params)):
            # Define the space between each event
            between_event_param = f"T_{i}_{i+1}"
            add_event_to_param(
                simple_div_params,
                between_event_param,
                space_between_events_min,
                space_between_events_max,
            )

            # add event to complex
            complex_div_params.append(
                f"1 {divergence_params[i]} = {between_event_param} + {divergence_params[i-1]} output"
            )
    return simple_div_params, complex_div_params


def get_admixture_event_params(admix_params, time_dist):
    return [
        "0 {} {} {} {} output".format(
            param, time_dist["type"], time_dist["min"], time_dist["max"]
        )
        for param in admix_params
    ]


def get_historical_event_params(tpl, time_dist, param_type):
    # TODO: check if there even are admix params
    divergence_params = []
    for element in get_params_from_tpl(tpl, "TDIV"):
        divergence_params.extend(re.findall(r"\bTDIV\w*", element))

    admixture_params = []
    for element in get_params_from_tpl(tpl, "TADMIX"):
        admixture_params.extend(re.findall(r"\bTADMIX\w*", element))

    simple_div_params, complex_div_params = get_divergence_event_params(
        divergence_params, time_dist
    )

    simple_admix_parmas = get_admixture_event_params(admixture_params, time_dist)

    simple_time_params = simple_div_params + simple_admix_parmas
    complex_time_params = complex_div_params

    if param_type == "simple":
        return simple_time_params
    else:
        return complex_time_params


def get_simple_params(
    tpl, mutation_rate_dist, effective_pop_size_dist, migration_dist, time_dist
):
    simple_params = []
    # get mutation rate params
    simple_params.extend(get_mutation_rate_params(mutation_rate_dist))

    # effective size params
    simple_params.extend(get_effective_size_params(tpl, effective_pop_size_dist))

    # get migration params
    simple_params.extend(get_migration_params(tpl, migration_dist))

    # get historical event params
    simple_params.extend(get_historical_event_params(tpl, time_dist, "simple"))
    return simple_params


def get_resize_params(tpl):
    complex_resize_params = []
    simple_params_to_add = []
    resize_lines_from_tpl = get_params_from_tpl(tpl, "RELANC")
    resize_params = [
        element
        for variable in resize_lines_from_tpl
        for element in variable.split()
        if element.startswith("RELANC")
    ]
    
    if resize_lines_from_tpl:
        simple_params_to_add = []
        # handle the first in the list
        first_resize_param = resize_params[0]
        sink_source = first_resize_param[len("RELANC"):]
        complex_resize_params.append(
            f"0 {first_resize_param} = N_ANCALL/N_ANC{sink_source} hide"
        )
        resize_params.remove(first_resize_param)
        simple_params_to_add.append("N_ANCALL")
        simple_params_to_add.append(f"N_ANC{sink_source}")
        # handle rest of the names
        for param in resize_params:
            sink_source = param[len("RELANC"):]
            
            complex_resize_params.append(
                f"0 {param} = N_ANC{sink_source[0]}{sink_source[1]}/NPOP_{sink_source[1]} hide"
            )
            simple_params_to_add.append(f"N_ANC{sink_source[0]}{sink_source[1]}")
        

    return complex_resize_params, simple_params_to_add


def get_complex_params(tpl, time_dist):
    complex_params = []

    # get resize params
    complex_resize_params, simple_params_to_add = get_resize_params(tpl)
    # need to add ancsize to simple params
    if complex_resize_params:
        complex_params.extend(complex_resize_params)

    # get complex time params
    complex_params.extend(get_historical_event_params(tpl, time_dist, "complex"))

    return complex_params, simple_params_to_add


def generate_random_params(
    tpl_filepath,
    est_filename,
    mutation_rate_dist,
    effective_pop_size_dist,
    migration_dist,
    time_dist,
):
    # convert tpl file to list
    tpl = []
    with open(tpl_filepath, "r") as tpl_file:
        for line in tpl_file:
            tpl.append(line.strip())

    # get simple params
    simple_params = get_simple_params(
        tpl=tpl,
        mutation_rate_dist=mutation_rate_dist,
        effective_pop_size_dist=effective_pop_size_dist,
        migration_dist=migration_dist,
        time_dist=time_dist,
    )

    # get complex params
    complex_params, simple_params_to_add = get_complex_params(
        tpl=tpl, time_dist=time_dist
    )
    if simple_params_to_add:
        for param in simple_params_to_add:
            simple_params.append(
                "1 {} {} {} {} output".format(
                    param,
                    effective_pop_size_dist["type"],
                    effective_pop_size_dist["min"],
                    effective_pop_size_dist["max"],
                )
            )

    # write to est
    write_est(simple_params, complex_params, est_filename)
