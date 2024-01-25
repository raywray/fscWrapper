import random

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

def randomize_divergence_order(root_population_indices, leaf_population_indices, *args):
    migrants = 1
    growth_rate = 0
    output = []
    possible_roots = root_population_indices.copy()
    possible_leaves = leaf_population_indices.copy()
    rev_migration_matrix_index = len(leaf_population_indices)

    while len(possible_leaves) > 0:
        root = random.sample(possible_roots, 1)
        offshoot = random.sample(possible_leaves, 1)
        root_name = population_name(index=root)
        offshoot_name = population_name(index=offshoot)
        time = f"TDIV_{root_name}to{offshoot_name}"
        new_deme_size = f"RES_{root_name}to{offshoot_name}"
        output.append(
            " ".join(map(str, [time, offshoot, root, migrants, new_deme_size, growth_rate, rev_migration_matrix_index]))
        )
        possible_roots.append(offshoot)
        possible_leaves.remove(offshoot)
        rev_migration_matrix_index -= 1

    return output

# # Assuming population_name function is defined elsewhere
# def population_name(index):
#     # Add your implementation of population_name
#     pass

def population_name(index):
    if index == 0:
        return "RAYA"
    else:
        return "TREVOR"
def matrix_generation(*args):
    return 0
def growth_rates(*args):
    return 0
def population_size(*args):
    return 0

def random_initializations():
    add_ghost = random.choice([True, False])
    split_SF = random.choice([True, False])
    num_pop = 3 if split_SF else 2
    num_pop += int(add_ghost)
    w_index = num_pop - (2 if add_ghost else 1)
    roots = [w_index]
    leaves = list(range(w_index))
    if add_ghost:
        ghost_role = random.choice(["root", "leaf"])
        if ghost_role == "root":
            roots.append(w_index+1)
        else:
            leaves.append(w_index+1)
    divergence_events = randomize_divergence_order(roots, leaves, split_SF=split_SF, ghost_present=add_ghost)
    historical_events = divergence_events
# Raya code here for migration matrix generation.
    mig_matrix=matrix_generation(num_pop, divergence_events, split_SF=split_SF)
    # Admixture code after divergence here.
    growth_rates=growth_rates(num_pop, historical_events, split_SF=split_SF)
    pop_name=population_name(0)
    pop_size=population_size(split_SF=split_SF)
    fn="sample.tpl"
    
    return write_tpl_file(fn, num_pop, pop_name, pop_size, ['0'] * len(growth_rates), mig_matrix, [f"{len(historical_events)} historical events"] + historical_events[::-1])

    

# TODO modify this function when the time comes

    

if NUM_OF_GROUPS==1:
    # NUM_OF_TOPOLOGIES=1
    write_est_file("test1.est","0","0")
    write_tpl_file("test2.tpl","0","0","0","0","0","0")
