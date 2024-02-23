import random
from math import comb
import re

NUM_OF_GROUPS = 1
TDIV = 0
TPLUS01 = 0
SAMPLE_SIZES = [1]
MUT_RATE = 6e-8


def write_est_file(file_name, simple_params, complex_params):
    lines = [
        "// Priors and rules file",
        "// *********************",
        "",
        "[PARAMETERS]",
        "0 MUTRATE unif 1e-7 1e-9 output",
        simple_params,
        "",
        "[COMPLEX PARAMETERS]",
        "",
        complex_params,
    ]

    with open(file_name, "w") as fout:
        fout.writelines("\n".join(lines))

def write_tpl_file(
    file_name, num_pops, Ne, sample_sizes, growth_rates, mig_info, historical_events
):
    # TODO will need to fix the population effective sizes and historical events

    def list_to_string(list):
        return " ".join(map(str, list))

    lines = [
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
        "FREQ 1 0 MUTRATE OUTEXP",
    ]

    with open(file_name, "w") as fout:
        fout.writelines("\n".join(lines))

def get_growth_rates(num_pops, events, **kwargs):  # TODO it looks like this function only ever returns 0s, so look into that
    gr = ["0"] * num_pops

    unique_matches = {
        match for event in events for match in re.findall(r"GR_[A-Z]+", event)
    }
    GR_ = list(unique_matches)
    population_order = population_name(**kwargs)
    for el in GR_:
        modified_code = el.replace("GR_", "")
        if modified_code in population_order:
            gr[population_order.index(modified_code)] = el
    return gr


def random_admixture_event(num_pops, divergence_event, **kwargs):
    source = my_sample(list(range(0, num_pops)), k=1)
    difference = list(set(list(range(0, num_pops))) - set([source]))
    sink = my_sample(difference, k=1)
    output = single_admixture_event(source, sink, divergence_event, **kwargs)
    output += single_admixture_event(sink, source, divergence_event, **kwargs)
    return output


def single_admixture_event(source, sink, divergence_event=None, **kwargs):
    # single admixture event following the divergence event
    if divergence_event is None:
        associated_matrix = [0]
    elif isinstance(divergence_event, (int, float)):
        associated_matrix = [divergence_event]
    elif "TDIV" in divergence_event:
        associated_matrix = re.sub(r"^T.* ([0-9])$", r"\1", divergence_event)
    else:
        return "Error in divergence event specification"
    source_name = population_name(index=source, **kwargs)
    sink_name = population_name(index=sink, **kwargs)
    event_name = f"TAdm_{sink_name}to{source_name}"
    migrants = f"a_{sink_name}to{source_name}"
    growth_rate = 0
    output = f"{event_name} {source} {sink} {migrants} 1 {growth_rate} {associated_matrix[0]} "
    return output


def population_size(index=None, split_SF=False, ghost_present=False):
    if not split_SF:
        sample_size = [6, 4]  # TODO this is hard-coded (6 society finches, 4 WRM)
    else:
        sample_size = [2, 4, 4]  # TODO this is also hard-coded
    if ghost_present:
        sample_size.append(0)
    if index is None:
        return sample_size
    return sample_size[index]


def current_migration_matrix(num_populations, **kwargs):
    current_matrix = ["//Migration matrix 0"]

    for i in range(1, num_populations + 1):
        matrix_row = []
        for j in range(1, num_populations + 1):
            if i == j:
                matrix_at_i_j = "0"
            else:
                from_pop = population_name(index=j - 1, **kwargs)
                to_pop = population_name(index=i - 1, **kwargs)
                matrix_at_i_j = f"MIG_{from_pop}to{to_pop}"

            matrix_row.append(matrix_at_i_j)
        current_matrix.append(" ".join(matrix_row))
    return current_matrix


def oldest_migration_matrix(num_populations):
    oldest_matrix = f"//Migration matrix {num_populations - 1}"
    temp = [["0"] * num_populations for _ in range(num_populations)]
    oldest_matrix = [oldest_matrix] + [" ".join(row) for row in temp]
    return oldest_matrix


def matrix_generation(num_pops, divergence_events, **kwargs):
    subsequent_matrix = current_migration_matrix(num_populations=num_pops, **kwargs)
    output = [subsequent_matrix]

    # # loop throught all divergence events to create matrices going backward in time
    for i in reversed(range(len(divergence_events))):
        event = divergence_events[i]
        subsequent_matrix_index = re.sub(r"T.* ([0-9])$", r"\1", event)
        if int(subsequent_matrix_index) == num_pops - 1:
            subsequent_matrix = oldest_migration_matrix(num_pops)
        else:
            coalescing_population = re.sub(
                r"^TDIV_[a-zA-Z]*to([a-zA-Z]*) [0-9].*$", r"\1", event
            )
            # do this to a matrix without the title element
            trimmed_matrix = subsequent_matrix.copy()
            trimmed_matrix.pop(0)
            pattern = r"MIG_{}to[A-Z]*|MIG_[A-Z]*to{}".format(
                coalescing_population, coalescing_population
            )
            subsequent_matrix = [re.sub(pattern, "0", line) for line in trimmed_matrix]
            title = f"//Migration matrix {subsequent_matrix_index}"
            subsequent_matrix.insert(0, title)

        output.append(subsequent_matrix)
    return output


def my_sample(x, **kwargs):
    if len(x) == 1:
        return x[0]
    else:
        return random.sample(x, **kwargs)[0]


def randomize_divergence_order(
    root_population_indices, leaf_population_indices, **kwargs
):
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
            " ".join(
                map(
                    str,
                    [
                        time,
                        offshoot,
                        root,
                        migrants,
                        new_deme_size,
                        growth_rate,
                        rev_migration_matrix_index,
                    ],
                )
            )
        )
        possible_roots.append(offshoot)
        possible_leaves.remove(offshoot)
        rev_migration_matrix_index -= 1

    return output


def population_name(index=None, split_SF=False, ghost_present=False):
    if not split_SF:
        populations = ["SF", "WRM"]
    else:
        populations = ["SFWC", "SFP", "WRM"]
    if ghost_present:
        populations.append("G")
    if index == None:
        index = list(range(len(populations)))
        return [populations[i] for i in index]
    return [
        populations[index]
    ]  # TODO does this have to return a list? can it return a string?


def random_initializations():
    # Determine if ghost pop
    add_ghost = random.choice([True, False])

    # determine total num of pops
    split_SF = random.choice([True, False])
    num_pops = 3 if split_SF else 2
    num_pops += int(add_ghost)

    # place wrm as root node (bc it's the outgroup)
    wrm_index = num_pops - (2 if add_ghost else 1)
    roots = [wrm_index]

    # place the society finch(es) as leaf nodes
    leaves = list(range(wrm_index))

    # place ghost pop (if there is one) as leaf or root
    if add_ghost:
        # determine if the ghost will be part of the root or leaf nodes in the tree
        ghost_role = random.choice(["root", "leaf"])
        if ghost_role == "root":
            roots.append(wrm_index + 1)
        else:
            leaves.append(wrm_index + 1)

    # create divergence events
    divergence_events = randomize_divergence_order(
        roots, leaves, split_SF=split_SF, ghost_present=add_ghost
    )
    historical_events = divergence_events

    # build migration matrices prior to each divergence event
    mig_mat = matrix_generation(
        num_pops, divergence_events, split_SF=split_SF, ghost_present=add_ghost
    )
    mig_info = [str(len(divergence_events) + 1)] + mig_mat

    # Was going to add admixing to periods after divergence
    # num_admixture_events <- sample(0:length(divergence_events), 1)
    # But example code only shows for the current period, so I'll do that
    # Admixture
    num_admixture_events = random.sample(range(comb(num_pops, 2) + 1), 1)[0]
    if num_admixture_events > 0:
        admix_after_these_divergences = [0] * num_admixture_events
        for i in range(1, num_admixture_events):
            admixture_event = random_admixture_event(
                num_pops,
                admix_after_these_divergences[i],  # TODO will this always be 0?
                split_SF=split_SF,
                ghost_present=add_ghost,
            )
            # don't repeat admix events
            while len(set(admixture_event) & set(historical_events)) > 0:
                admixture_event = random_admixture_event(
                    num_pops,
                    admix_after_these_divergences[i],  # TODO will this always be 0?
                    split_SF=split_SF,
                    ghost_present=add_ghost,
                )
            historical_events.append(admixture_event)

    # pull growth rates from hx events
    growth_rates = get_growth_rates(
        num_pops, events=historical_events, split_SF=split_SF, ghost_present=add_ghost
    )

    # Effective population sizes
    Ne = f"NPOP_{population_name(split_SF=split_SF, ghost_present=add_ghost)}"

    # Sample sizes
    sample_sizes = population_size(split_SF=split_SF, ghost_present=add_ghost)
    file_name = "sample.tpl"

    return write_tpl_file(
        file_name=file_name,
        num_pops=num_pops,
        Ne=Ne,
        sample_sizes=sample_sizes,
        growth_rates=["0"] * len(growth_rates),
        mig_info=mig_info,
        historical_events=[f"{len(historical_events)} historical events"]
        + historical_events[::-1],
    )


# TODO modify this function when the time comes
# random_initializations()
# TODO write create_est function
# if NUM_OF_GROUPS==1:
#     # NUM_OF_TOPOLOGIES=1
#     write_est_file("test1.est","0","0")
#     write_tpl_file("test2.tpl","0","0","0","0","0","0")
