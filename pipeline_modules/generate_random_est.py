import re
from itertools import chain


def estimation(simple_params, complex_params, mutation_rate_dist):
    return (
        [
            "// Priors and rules file",
            "// *********************",
            "",
            "[PARAMETERS]",
            "//#isInt? #name #dist. #min #max",
            f"0 MUTRATE {mutation_rate_dist["type"]} {mutation_rate_dist["min"]} {mutation_rate_dist["max"]} output",
        ]
        + [param for param in simple_params]
        + [
            "",
            "[COMPLEX PARAMETERS]",
            "",
        ]
        + [param for param in complex_params]
    )


def get_population_parameters(input_template, ne_dist):
    population_parameters = [line for line in input_template if "NPOP_" in line]
    formatted_population_parameters = [
        "1 {} {} {} {} output".format(param, ne_dist["type"], ne_dist["min"], ne_dist["max"])
        for param in population_parameters
    ]
    return formatted_population_parameters


def get_migration_parameters(input_template):
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
        "0 " + param + " logunif 1e-10 1e-1 output"
        for param in current_migration_parameters
    ]
    return migration_parameters


def get_parameter_pattern(prefix):
    return rf"{prefix}_[a-zA-Z0-9]+"


def resize_parameters(input_template, resized_dist):
    resized_parameters = []
    if any("RES_" in line for line in input_template):
        resize_parameters = set(
            re.findall(get_parameter_pattern("RES"), " ".join(input_template))
        )
        resized_parameters = [
            "0 {} {} {} {} output".format(param, resized_dist["type"], resized_dist["min"], resized_dist["max"])
            for param in resize_parameters
        ]
    return resized_parameters


def get_admixture_parameters(input_template, admix_dist):
    admixture_parameters = set(
        re.findall(get_parameter_pattern("a"), " ".join(input_template))
    )
    formatted_admixture_parameters = [
        "0 {} {} {} {} output".format(param, admix_dist["type"], admix_dist["min"], admix_dist["max"]) 
        for param in admixture_parameters
    ]
    return formatted_admixture_parameters


def get_time_parameters(input_template):
    simple_time_parameters = []
    complex_time_parameters = []

    # Find all occurrences of time parameters (TDIV or TAdm) in the input template
    time_parameter_locations = [
        i for i, item in enumerate(input_template) if re.search("TDIV|TAdm", item)
    ]
    time_pattern = get_parameter_pattern("^(TDIV|TAdm)")
    time_parameters = [
        re.match(time_pattern, input_template[i]).group()
        for i in time_parameter_locations
        if re.match(time_pattern, input_template[i])
    ]

     # Handle the time space between each event
    if len(time_parameters) == 1:
        simple_time_parameters.append(f"1 {time_parameters[0]} unif 1 5000 output")
    elif len(time_parameters) > 1:
        simple_time_parameters.append(f"1 {time_parameters[0]} unif 1 600 output")
        for i in range(1, len(time_parameters)):
            # Define the space between each event
            extra_time_parameter = f"T_{i}_{i+1}"
            simple_time_parameters.append(f"1 {extra_time_parameter} unif 0 500 hide")
            complex_time_parameters.append(
                f"1 {time_parameters[i]} = {extra_time_parameter} + {time_parameters[i-1]} output"
            )
    return simple_time_parameters, complex_time_parameters


# this function generates an estimation file for a tpl template
def create_est(
        input_template_filepath, 
        est_filename="random.est", 
        mutation_rate_dist={}, 
        ne_dist={},
        resized_dist={},
        admix_dist={}
):
    input_template = []

    with open(input_template_filepath, "r") as inFile:
        for line in inFile:
            input_template.append(line.strip())

    # Initialize lists for parameters
    simple_parameters = []
    complex_parameters = []

    # Population parameters
    simple_parameters.extend(get_population_parameters(input_template, ne_dist))

    # Migration rate parameters
    simple_parameters.extend(get_migration_parameters(input_template))

    # Resizing parameters
    simple_parameters.extend(resize_parameters(input_template, resized_dist))

    # Time parameters
    simple_time_parameters, complex_time_parameters = get_time_parameters(input_template)
    simple_parameters.extend(simple_time_parameters)
    complex_parameters.extend(complex_time_parameters)

    # Admixture parameters
    simple_parameters.extend(get_admixture_parameters(input_template, admix_dist))

    # Combine parameters & write to a file
    est = estimation(simple_parameters, complex_parameters, mutation_rate_dist)
    with open(est_filename, "w") as file:
        for line in est:
            file.write(line + "\n")
