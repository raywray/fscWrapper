NUM_OF_GROUPS=1
TDIV=0
TPLUS01=0
SAMPLE_SIZES=[1]
MUT_RATE=6e-8

def write_est_file(file_name, simple_params, complex_params):
    lines=[
        "// Priors and rules file",
        "// *********************",
        "",
        "[PARAMETERS]",
        "0 MUTRATE unif 1e-7 1e-9 output",
        simple_params,
        "",
        "[COMPLEX PARAMETERS]",
        "",
        complex_params
    ]
    
    with open(file_name,"w") as fout:
        fout.writelines('\n'.join(lines))

def write_tpl_file(file_name, num_pops, Ne, sample_sizes, growth_rates, mig_info, historical_events):
    lines=[
        "//Number of population samples (demes)",
        num_pops,
        "//Population effective sizes (number of genes)",
        Ne,
        "//Sample sizes",
        sample_sizes,
        "//Growth rates : negative growth implies population expansion",
        growth_rates,
        "//Number of migration matrices : 0 implies no migration between demes",
        mig_info,
        "//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index",
        historical_events,
        "//Number of independent loci [chromosome]",
        "1 0",
        "//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci",
        "1",
        "//per Block:data type, number of loci, per gen recomb and mut rates",
        "FREQ 1 0 MUTRATE OUTEXP"
    ]

    with open(file_name,"w") as fout:
        fout.writelines('\n'.join(lines))
        
    
def current_migration_matrix(num_populations, *args):
    current_matrix = ["//Migration matrix 0"]
    
    for i in range(1, num_populations + 1):
        matrix_row = []
        for j in range(1, num_populations + 1):
            if i == j:
                matrix_at_i_j = "0"
            else:
                from_pop = population_name(index = j-1, *args)
                to_pop = population_name(index = i-1, *args)
                matrix_at_i_j = f"MIG_{from_pop}to{to_pop}"
                
            matrix_row.append(matrix_at_i_j)
        current_matrix.append(" ".join(matrix_row))
    return(current_matrix)


def oldest_migration_matrix(num_populations):
    oldest_matrix = f"//Migration matrix {num_populations - 1}"
    temp = [["0"] * num_populations for _ in range(num_populations)]
    oldest_matrix = [oldest_matrix] + [" ".join(row) for row in temp]
    return oldest_matrix


# TODO modify this function when the time comes
def population_name(index):
    if index == 0:
        return "RAYA"
    else:
        return "TREVOR"
    

if NUM_OF_GROUPS==1:
    # NUM_OF_TOPOLOGIES=1
    write_est_file("test1.est","0","0")
    write_tpl_file("test2.tpl","0","0","0","0","0","0")
