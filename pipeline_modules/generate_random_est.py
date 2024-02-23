import re

# this function generates an estimation file for a tpl template
def create_est(input_template):
    # TODO open input template file
    simple_parameters = []
    complex_parameters = []

    # effective pop size params
    population_parameters = [ne for ne in input_template if re.search("NPOP_", ne)]
    formatted_number = f"{30*10**4}"
    # TODO rename append_me
    append_me = [f"1 {param} unif 100 {formatted_number} output" for param in population_parameters]
    simple_parameters.append(append_me)
    print(simple_parameters)

    

    return 0

tpl = [
    "//Parameters for the coalescence simulation program : simcoal.exe",
    "2 samples to simulate :",
    "//Population effective sizes (number of genes)",
    "NPOP_1",
    "NPOP_2",
    "//Samples sizes and samples age",
    "6",
    "4",
    "//Growth rates: negative growth implies population expansion",
    "GROWTH1",
    "GROWTH2",
    "//Number of migration matrices : 0 implies no migration between demes",
    "1",
    "//Migration matrix 0",
    "0 MIG2",
    "MIG1 0",
    "//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index",
    "1 historical event",
    "TDIV 0 0 0 RESIZE 0 0",
    "//Number of independent loci [chromosome]",
    "1 0",
    "//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci",
    "1",
    "//per Block:data type, number of loci, per gen recomb and mut rates",
    "FREQ 1 0 2.5e-8",
]
create_est(tpl)

#  "1 NPOP_1 unif 100 300000 output" "1 NPOP_2 unif 100 300000 output"