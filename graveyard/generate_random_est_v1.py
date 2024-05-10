import re
from itertools import chain


def populate_est(simple_params, complex_params, mutation_rate_dist):
    return (
        [
            "// Priors and rules file",
            "// *********************",
            "",
            "[PARAMETERS]",
            "//#isInt? #name #dist. #min #max",
            "0 MUTRATE {} {} {} output".format(
                mutation_rate_dist["type"],
                mutation_rate_dist["min"],
                mutation_rate_dist["max"],
            ),
        ]
        + [param for param in simple_params]
        + [
            "",
            "[COMPLEX PARAMETERS]",
            "",
        ]
        + [param for param in complex_params]
    )


def get_population_params_from_tpl(input_template):
    return [line for line in input_template if "NPOP_" in line]


def get_population_parameters(input_template, ne_dist):
    population_parameters = get_population_params_from_tpl(input_template)
    formatted_population_parameters = [
        "1 {} {} {} {} output".format(
            param, ne_dist["type"], ne_dist["min"], ne_dist["max"]
        )
        for param in population_parameters
    ]
    return formatted_population_parameters

# TODO:this is the way I tried following Arun's code
# def get_resize_parameters(input_template, resize_dist):
#     population_params = get_population_params_from_tpl(input_template)
#     resize_params = []
#     for pop in population_params:
#         pop_number = pop.split("_")[1]
#         resize_params.append(
#             "0 {} {} {} {} hide".format(
#                 f"N{pop_number}RESIZE",
#                 resize_dist["type"],
#                 resize_dist["min"],
#                 resize_dist["max"],
#             )
#         )
#     return resize_params

def is_population_expanding(input_template):
    # find the growth rates
    start_index = (
        input_template.index(
            "//Growth rates : negative growth implies population expansion"
        )
        + 1
    )
    end_index = input_template.index(
        "//Number of migration matrices : 0 implies no migration between demes"
    )
    growth_rates = input_template[start_index:end_index]

    if growth_rates[0] != "0":
        return True
    else:
        return False


def get_growth_rate_params(input_template):
    population_params = get_population_params_from_tpl(input_template)
    
    all_splits = []
    ratios = []
    logs = []
    growths = []
    
    time_params = get_time_params_from_tpl(input_template)
    
    for pop in population_params:
        pop_number = pop.split("_")[1]
        
        all_splits.append(
            f"1 N{pop_number}atSPLIT = {pop}*N{pop_number}RESIZE output"
        )
        
        ratios.append(f"0 tmpRATIOP{pop_number} = N{pop_number}atSPLIT/{pop} hide")
        
        logs.append(f"0 tmplogP{pop_number} = log(tmpRATIOP{pop_number}) hide")
        
        growths.append(
            f"0 GrowthP{pop_number} = tmplogP{pop_number}/{time_params[0]} output"
        )

    return all_splits + ratios + logs + growths


def get_migration_parameters(input_template, mig_dist):
    # get parameters from the migraion matrix 0
    migration_matrix_0_location = [
        i
        for i, item in enumerate(input_template)
        if re.search("Migration matrix 0", item)
    ][0] + 1
    migration_matrix_1_location = [
        i
        for i, item in enumerate(input_template)
        if re.search("Migration matrix 1", item)
    ][0]

    current_migration_parameter_location = input_template[
        migration_matrix_0_location:migration_matrix_1_location
    ]

    # extract only the MIG_POP information
    current_migration_parameters = sorted(
        list(
            set(
                chain.from_iterable(
                    [item.split(" ") for item in current_migration_parameter_location]
                )
            )
        )
    )[1:]

    # create migration parameters
    migration_parameters = [
        "0 {} {} {} {} output".format(
            param, mig_dist["type"], mig_dist["min"], mig_dist["max"]
        )
        for param in current_migration_parameters
    ]
    return migration_parameters

# TODO: this is from stephanie's NEW code
# Resizing parameters (past population size / future population size)
def get_res_parameters(input_template, res_dist):
    res_params = []
    if any("RES_" in line for line in input_template):
        res_params_from_tpl = set(
            re.findall(get_parameter_pattern("RES"), " ".join(input_template))
        )
        res_params = [
            "0 {} {} {} {} output".format(
                param, res_dist["type"], res_dist["min"], res_dist["max"]
            )
            for param in res_params_from_tpl
        ]
    return res_params


def get_parameter_pattern(prefix):
    return rf"{prefix}_[a-zA-Z0-9]+"


def get_admixture_parameters(input_template, admix_dist):
    admixture_parameters = set(
        re.findall(get_parameter_pattern("a"), " ".join(input_template))
    )
    formatted_admixture_parameters = [
        "0 {} {} {} {} output".format(
            param, admix_dist["type"], admix_dist["min"], admix_dist["max"]
        )
        for param in admixture_parameters
    ]
    return formatted_admixture_parameters


def get_time_params_from_tpl(input_template):
    time_parameter_locations = [
        i for i, item in enumerate(input_template) if re.search("TDIV|TAdm", item)
    ]
    time_pattern = get_parameter_pattern("^(TDIV|TAdm)")
    time_parameters = [
        re.match(time_pattern, input_template[i]).group()
        for i in time_parameter_locations
        if re.match(time_pattern, input_template[i])
    ]

    return time_parameters


def get_time_parameters(input_template, time_dist):
    simple_time_parameters = []
    complex_time_parameters = []

    # Find all occurrences of time parameters (TDIV or TAdm) in the input template
    time_parameters = get_time_params_from_tpl(input_template)

    # Handle the time space between each event
    if len(time_parameters) == 1:
        simple_time_parameters.append(
            "1 {} {} {} {} output".format(
                time_parameters[0],
                time_dist["type"],
                time_dist["single_min"],
                time_dist["single_max"],
            )
        )
    elif len(time_parameters) > 1:
        simple_time_parameters.append(
            "1 {} {} {} {} output".format(
                time_parameters[0],
                time_dist["type"],
                time_dist["multiple_min"],
                time_dist["multiple_max"],
            )
        )
        for i in range(1, len(time_parameters)):
            # Define the space between each event
            extra_time_parameter = f"T_{i}_{i+1}"
            simple_time_parameters.append(
                "1 {} {} {} {} hide".format(
                    extra_time_parameter,
                    time_dist["type"],
                    time_dist["extra_min"],
                    time_dist["extra_max"],
                )
            )
            complex_time_parameters.append(
                f"1 {time_parameters[i]} = {extra_time_parameter} + {time_parameters[i-1]} output"
            )
    return simple_time_parameters, complex_time_parameters


# this function generates an estimation file for a tpl template
def create_est(
    input_template_filepath,
    est_filename="random.est",
    mutation_rate_dist={},
    effective_pop_size_dist={},
    admix_dist={},
    res_dist={}, #TODO: maybe uncomment
    migration_dist={},
    time_dist={},
    # resize_dist={},
):
    input_template = []

    with open(input_template_filepath, "r") as inFile:
        for line in inFile:
            input_template.append(line.strip())

    # Initialize lists for parameters
    simple_parameters = []
    complex_parameters = []

    # Population parameters
    simple_parameters.extend(get_population_parameters(input_template, effective_pop_size_dist))

    # Resize parameters ONLY if expansion TODO: reconsider
    # should_pop_expand = is_population_expanding(input_template)
    # if should_pop_expand:
    #     simple_parameters.extend(get_resize_parameters(input_template, resize_dist))

    # Migration rate parameters
    simple_parameters.extend(get_migration_parameters(input_template, migration_dist))
    
    # Resize parameters
    simple_parameters.extend(get_res_parameters(input_template, res_dist)) # TODO: maybe uncomment

    # Time parameters
    simple_time_parameters, complex_time_parameters = get_time_parameters(
        input_template, time_dist
    )
    simple_parameters.extend(simple_time_parameters)
    complex_parameters.extend(complex_time_parameters)

    # Admixture parameters
    simple_parameters.extend(get_admixture_parameters(input_template, admix_dist))

    # Growth rate params, only if population is expanding
    should_pop_expand = is_population_expanding(input_template)
    if should_pop_expand:
        complex_parameters.extend(get_growth_rate_params(input_template))

    # Combine parameters & write to a file
    est = populate_est(simple_parameters, complex_parameters, mutation_rate_dist)
    with open(est_filename, "w") as file:
        for line in est:
            file.write(line + "\n")