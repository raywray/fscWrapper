import re
from itertools import chain


def estimation(simple_params, complex_params):
    return (
        [
            "//Priors and rules file",
            "// *********************",
            "",
            "[PARAMETERS]",
            "0 MUTRATE unif 1e-7 1e-9 output",
        ]
        + [param for param in simple_params]
        + [
            "",
            "[COMPLEX PARAMETERS]",
            "",
        ]
        + [param for param in complex_params]
    )


# this function generates an estimation file for a tpl template
def create_est(input_template_filepath, est_filename="random.est"):
    input_template = []

    with open(input_template_filepath, "r") as inFile:
        for line in inFile:
            input_template.append(line.strip())

    # Initialize lists for parameters
    simple_parameters = []
    complex_parameters = []

    # Population parameters
    population_parameters = [line for line in input_template if "NPOP_" in line]
    formatted_number = "{:,}".format(30 * 10**4).replace(",", "")
    append_me = [
        "1 {} unif 100 {} output".format(param, formatted_number)
        for param in population_parameters
    ]
    simple_parameters.extend(append_me)

    # Migration rate parameters
    migration_matrix_0_location = [i for i, item in enumerate(input_template) if re.search("Migration matrix 0", item)][0] + 1
    migration_matrix_1_location = [i for i, item in enumerate(input_template) if re.search("Migration matrix 1", item)][0]

    current_migration_parameter_location = input_template[migration_matrix_0_location:migration_matrix_1_location]
    current_migration_parameters = list(set(chain.from_iterable([item.split(" ") for item in current_migration_parameter_location])))[1:]

    append_me = ["0 " + param + " logunif 1e-10 1e-1 output" for param in current_migration_parameters] # TODO rename this
    simple_parameters.extend(append_me)

    # Resizing parameters
    if any("RES_" in line for line in input_template):
        resize_parameters = set(
            re.findall(r"(RES_[a-zA-Z0-9_]+)", " ".join(input_template))
        )
        append_me = [
            "0 {} unif 0 100 output".format(param) for param in resize_parameters
        ]
        simple_parameters.extend(append_me)

    # Time parameters
    # Find all occurrences of time parameters (TDIV or TAdm) in the input template
    time_parameter_locations = [i for i, item in enumerate(input_template) if re.search("TDIV|TAdm", item)]
    time_parameters = [re.match("^(T[a-zA-Z_]*) .*$", input_template[i]).groups()[0] for i in time_parameter_locations]

    # Handle the time space between each event
    if len(time_parameters) == 1:
        simple_parameters.append(f"1 {time_parameters[0]} unif 1 5000 output")
    elif len(time_parameters) > 1:
        simple_parameters.append(f"1 {time_parameters[0]} unif 1 600 output")
        for i in range(1, len(time_parameters)):
            # Define the space between each event
            extra_time_parameter = f"T_{i}_{i+1}"
            simple_parameters.append(f"1 {extra_time_parameter} unif 0 500 hide")
            complex_parameters.append(f"1 {time_parameters[i]} = {extra_time_parameter} + {time_parameters[i-1]} output")

    # Admixture parameters
    admixture_parameters = set(
        re.findall(r"(a_[a-zA-Z0-9_]+)", " ".join(input_template))
    )
    append_me = [ # TODO rename this
        "0 {} unif 0 0.25 output".format(param) for param in admixture_parameters
    ]
    simple_parameters.extend(append_me)

    # Combine parameters & write to a file
    est = estimation(simple_parameters, complex_parameters)
    with open(est_filename, "w") as file:
        for line in est:
            file.write(line + "\n")