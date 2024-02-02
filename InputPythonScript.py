import random
from math import comb

NUM_OF_GROUPS=1
TDIV=0
TPLUS01=0
SAMPLE_SIZES=[1]
MUT_RATE=6e-8

def matrix_generation(num_pops, divergence_events, **kwargs):
    return []
def get_growth_rates(num_pops, **kwargs):
    return [0, 6, 5]
def population_size(**kwargs):
    return 0

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
    # TODO will need to fix the population effective sizes and historical events
    
    def list_to_string(list):
        return " ".join(map(str, list))
    
    lines=[
        "//Number of population samples (demes)",
        str(num_pops),
        "//Population effective sizes (number of genes)",
        str(Ne),
        "//Sample sizes",
        str(sample_sizes),
        "//Growth rates : negative growth implies population expansion",
        list_to_string(growth_rates),
        "//Number of migration matrices : 0 implies no migration between demes",
        list_to_string(mig_info),
        "//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index",
        list_to_string(historical_events),
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

def my_sample(x, **kwargs):
    if len(x) == 1:
        return x[0]
    else:
        return random.sample(x, **kwargs)[0]

def randomize_divergence_order(root_population_indices, leaf_population_indices, **kwargs):
    migrants = 1
    growth_rate = 0
    output = []
    possible_roots = root_population_indices.copy()
    possible_leaves = leaf_population_indices.copy()
    rev_migration_matrix_index = len(leaf_population_indices)

    while len(possible_leaves) > 0:
        root = my_sample(possible_roots, k=1)
        offshoot = my_sample(possible_leaves, k=1)
        root_name = population_name(index=root, **kwargs)
        offshoot_name = population_name(index=offshoot, **kwargs)
        time = f"TDIV_{root_name}to{offshoot_name}"
        new_deme_size = f"RES_{root_name}to{offshoot_name}"
        output.append(
            " ".join(map(str, [time, offshoot, root, migrants, new_deme_size, growth_rate, rev_migration_matrix_index]))
        )
        possible_roots.append(offshoot)
        possible_leaves.remove(offshoot)
        rev_migration_matrix_index -= 1

    return output

def population_name(index = None, split_SF=False, ghost_present=False):
    if not split_SF:
        populations = ["SF", "WRM"]
    else:
        populations = ["SFWC", "SFP", "WRM"]
    if ghost_present:
        populations.append("G")
    if index == None:
        index = list(range(len(populations)))
        return [populations[i] for i in index]
    return [populations[index]]

def get_admixture_event(num_admixture_events):
    return []

def random_initializations():
    add_ghost = random.choice([True, False])
    split_SF = random.choice([True, False])
    num_pops = 3 if split_SF else 2
    num_pops += int(add_ghost)
    w_index = num_pops - (2 if add_ghost else 1)
    roots = [w_index] 
    leaves = list(range(w_index))
    if add_ghost:
        ghost_role = random.choice(["root", "leaf"])
        if ghost_role == "root":
            roots.append(w_index + 1)
        else:
            leaves.append(w_index + 1)
   
    divergence_events = randomize_divergence_order(roots, leaves, split_SF=split_SF, ghost_present=add_ghost)
    historical_events = divergence_events

    mig_mat=matrix_generation(num_pops, divergence_events, split_SF=split_SF, ghost_present=add_ghost)
    mig_info = [str(len(divergence_events) + 1)] + mig_mat
    # Admixture
    num_admixture_events = random.sample(range(comb(num_pops, 2) + 1), 1)[0]
    historical_events.append(get_admixture_event(num_admixture_events))
    
    # Admixture code after divergence here.
    growth_rates=get_growth_rates(num_pops, events=historical_events, split_SF=split_SF, ghost_present=add_ghost)
    
    # Effective population sizes
    Ne = f"NPOP_{population_name(split_SF=split_SF, ghost_present=add_ghost)}"

    # Sample sizes
    sample_sizes = population_size(split_SF=split_SF, ghost_present = add_ghost)
    file_name="sample.tpl"
    
    return write_tpl_file(file_name=file_name, num_pops=num_pops, Ne=Ne, sample_sizes=sample_sizes, growth_rates=['0'] * len(growth_rates), mig_info=mig_info, historical_events=[f"{len(historical_events)} historical events"] + historical_events[::-1])

    

# TODO modify this function when the time comes
random_initializations()
# if NUM_OF_GROUPS==1:
#     # NUM_OF_TOPOLOGIES=1
#     write_est_file("test1.est","0","0")
#     write_tpl_file("test2.tpl","0","0","0","0","0","0")