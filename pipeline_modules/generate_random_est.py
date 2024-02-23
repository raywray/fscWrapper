import re

def estimation(simple_params, complex_params):
    return [
        "//Priors and rules file",
        "// *********************",
        "",
        "[PARAMETERS]",
        "0 MUTRATE unif 1e-7 1e-9 output",
        f"{simple_params}",
        "",
        "[COMPLEX PARAMETERS]",
        "",
        f"{complex_params}"
        ]

# this function generates an estimation file for a tpl template
def create_est(input_template):
    # Initialize lists for parameters
    simple_parameters = []
    complex_parameters = []

    # Population parameters
    population_parameters = [line for line in input_template if "NPOP_" in line]
    formatted_number = "{:,}".format(30 * 10**4).replace(',', '')
    append_me = ["1 {} unif 100 {} output".format(param, formatted_number) for param in population_parameters]
    simple_parameters.extend(append_me)

    # Migration rate parameters
    start_idx = next((i for i, item in enumerate(input_template) if "Migration matrix 0" in item), None) + 1
    end_idx = next((i for i, item in enumerate(input_template) if "Migration matrix 1" in item), None) - 1
    if start_idx and end_idx:
        current_migration_parameters = set(" ".join(input_template[start_idx:end_idx]).split())
        append_me = ["0 {} logunif 1e-10 1e-1 output".format(param) for param in current_migration_parameters if param != "0"]
        simple_parameters.extend(append_me)

    # Resizing parameters
    if any("RES_" in line for line in input_template):
        resize_parameters = set(re.findall(r'(RES_[a-zA-Z0-9_]+)', " ".join(input_template)))
        append_me = ["0 {} unif 0 100 output".format(param) for param in resize_parameters]
        simple_parameters.extend(append_me)

    # Time parameters
    time_parameters = set(re.findall(r'^(T(DIV|Adm)_[a-zA-Z0-9_]+)', " ".join(input_template)))
    append_me = ["1 {} unif 1 5000 output".format(param) for param in time_parameters]
    simple_parameters.extend(append_me)

    # Admixture parameters
    admixture_parameters = set(re.findall(r'(a_[a-zA-Z0-9_]+)', " ".join(input_template)))
    append_me = ["0 {} unif 0 .25 output".format(param) for param in admixture_parameters]
    simple_parameters.extend(append_me)

    # Return combined parameters
    return estimation(simple_parameters, complex_parameters)

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
  "FREQ 1 0 MUTRATE OUTEXP"
]
est = create_est(tpl)
with open("is-this-right.est", "w") as file:
    file.writelines(est)
