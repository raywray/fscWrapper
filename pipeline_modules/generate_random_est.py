import re


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
def create_est(input_template):
    # TODO change to read in a file
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
    # TODO this is where the simple params error is
    start_idx = (
        next(
            (
                i
                for i, item in enumerate(input_template)
                if "Migration matrix 0" in item
            ),
            None,
        )
        + 1
    )
    end_idx = (
        next(
            (
                i
                for i, item in enumerate(input_template)
                if "Migration matrix 1" in item
            ),
            None,
        )
        - 1
    )
    if start_idx and end_idx:
        current_migration_parameters = set(
            " ".join(input_template[start_idx:end_idx]).split()
        )
        append_me = [
            "0 {} logunif 1e-10 1e-1 output".format(param)
            for param in current_migration_parameters
            if param != "0"
        ]
        simple_parameters.extend(append_me)
        print("simple param")
        for param in simple_parameters: print(param)

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
    append_me = [
        "0 {} unif 0 .25 output".format(param) for param in admixture_parameters
    ]
    simple_parameters.extend(append_me)

    # Combine parameters & write to a file
    est = estimation(simple_parameters, complex_parameters)
    with open("random.est", "w") as file:
        for line in est:
            file.write(line + "\n")


tpl = [
    "//Number of population samples (demes)",
    "4",
    "//Population effective sizes (number of genes)",
    "NPOP_SFWC",
    "NPOP_SFP",
    "NPOP_WRM",
    "NPOP_G",
    "//Sample sizes",
    "2",
    "4",
    "4",
    "0",
    "//Growth rates : negative growth implies population expansion",
    "0",
    "0",
    "0",
    "0",
    "//Number of migration matrices : 0 implies no migration between demes",
    "3",
    "//Migration matrix 0",
    "0 MIG_SFPtoSFWC MIG_WRMtoSFWC MIG_GtoSFWC",
    "MIG_SFWCtoSFP 0 MIG_WRMtoSFP MIG_GtoSFP",
    "MIG_SFWCtoWRM MIG_SFPtoWRM 0 MIG_GtoWRM",
    "MIG_SFWCtoG MIG_SFPtoG MIG_WRMtoG 0",
    "//Migration matrix 1",
    "0 0 MIG_WRMtoSFWC MIG_GtoSFWC",
    "0 0 0 0",
    "MIG_SFWCtoWRM 0 0 MIG_GtoWRM",
    "MIG_SFWCtoG 0 MIG_WRMtoG 0",
    "//Migration matrix 2",
    "0 0 0 0",
    "0 0 0 0",
    "0 0 0 MIG_GtoWRM",
    "0 0 MIG_WRMtoG 0",
    "//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index",
    "8 historical events",
    "TAdm_WRMtoSFWC 0 2 a_WRMtoSFWC 1 0 0",
    "TAdm_SFWCtoWRM 2 0 a_SFWCtoWRM 1 0 0",
    "TAdm_GtoSFWC 0 3 a_GtoSFWC 1 0 0",
    "TAdm_SFWCtoG 3 0 a_SFWCtoG 1 0 0",
    "TAdm_GtoWRM 2 3 a_GtoWRM 1 0 0",
    "TAdm_WRMtoG 3 2 a_WRMtoG 1 0 0",
    "TDIV_WRMtoSFP 1 2 1 RES_WRMtoSFP 0 1",
    "TDIV_WRMtoSFWC 0 2 1 RES_WRMtoSFWC 0 2",
    "//Number of independent loci [chromosome]",
    "1 0",
    "//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci",
    "1",
    "//per Block:data type, number of loci, per gen recomb and mut rates",
    "FREQ 1 0 MUTRATE OUTEXP",
]
create_est(tpl)

# [1] "simple params"
#  [1] "1 NPOP_SFWC unif 100 300000 output"       
#  [2] "1 NPOP_SFP unif 100 300000 output"        
#  [3] "1 NPOP_WRM unif 100 300000 output"        
#  [4] "1 NPOP_G unif 100 300000 output"          
#  [5] "0 MIG_SFPtoSFWC logunif 1e-10 1e-1 output"
#  [6] "0 MIG_WRMtoSFWC logunif 1e-10 1e-1 output"
#  [7] "0 MIG_GtoSFWC logunif 1e-10 1e-1 output"  
#  [8] "0 MIG_SFWCtoSFP logunif 1e-10 1e-1 output"
#  [9] "0 MIG_WRMtoSFP logunif 1e-10 1e-1 output" 
# [10] "0 MIG_GtoSFP logunif 1e-10 1e-1 output"   
# [11] "0 MIG_SFWCtoWRM logunif 1e-10 1e-1 output"
# [12] "0 MIG_SFPtoWRM logunif 1e-10 1e-1 output" 
# [13] "0 MIG_GtoWRM logunif 1e-10 1e-1 output"   
# [14] "0 MIG_SFWCtoG logunif 1e-10 1e-1 output"  
# [15] "0 MIG_SFPtoG logunif 1e-10 1e-1 output"   
# [16] "0 MIG_WRMtoG logunif 1e-10 1e-1 output"   