import random
import re


def write_tpl(
    filename,
    number_of_populations,
    population_effective_sizes,
    sample_sizes,
    growth_rates,
    migration_matrices,
    historical_events,
):
    flattened_migration_matrices = []
    for matrix in migration_matrices:
        for line in matrix:
            flattened_migration_matrices.append(line)
    lines = [
        "//Number of population samples (demes)",
        str(number_of_populations),
        "//Population effective sizes (number of genes)",
        *population_effective_sizes,
        "//Sample Sizes",
        *[str(size) for size in sample_sizes],
        "//Growth rates : negative growth implies population expansion",
        *[str(size) for size in growth_rates],
        "//Number of migration matrices : 0 implies no migration between demes",
        str(len(migration_matrices)),
        *flattened_migration_matrices,
        "//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index",
        f"{len(historical_events)} historical event",
        *historical_events,
        "//Number of independent loci [chromosome]",
        "1 0",
        "//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci",
        "1",
        "//per Block:data type, number of loci, per gen recomb and mut rates",
        f"FREQ 1 0 MUTRATE OUTEXP",
    ]

    # write to file
    with open(filename, "w") as tpl_file:
        tpl_file.writelines("\n".join(lines))


def get_population_list(num_pops, ghost_present):
    populations = []
    population_range = num_pops - 1 if ghost_present else num_pops

    for i in range(0, population_range):
        populations.append(str(i))

    if ghost_present:
        populations.append("G")
    return populations


def get_population_effective_sizes(number_of_populations, ghost_present):
    return [
        f"N_POP{i}" for i in get_population_list(number_of_populations, ghost_present)
    ]


# TODO: delete?
def get_random_growth_rate():
    # according to my research, this is often 0.
    # Generate a random number between 0 and 1
    rand = random.random()
    if rand < 0.9:
        return 0  # Return 0 with a probability of 90%
    else:
        return random.uniform(
            -1, 1
        )  # Return a random value between -1 and 1 with a probability of 10%


# TODO: will need to look at this again when putting more complex events back in
def get_sources_and_sinks(ghost_present, number_of_populations):
    possible_sources = list(range(number_of_populations))
    possible_sinks = list(range(number_of_populations))

    if ghost_present:
        possible_sources.pop(-1)
        possible_sinks.pop(-1)

        # determine if ghost is source or sink
        if random.choice([True, False]):
            possible_sources.append("G")
        else:
            possible_sinks.append("G")

    sources = []
    for _ in range(random.randint(1, number_of_populations)):
        if possible_sources == []:
            break
        new_source = random.choice(possible_sources)
        sources.append(str(new_source))
        possible_sources.remove(new_source)

    sinks = []
    for _ in range(random.randint(1, number_of_populations)):
        if possible_sinks == []:
            break
        new_sink = random.choice(possible_sinks)
        sinks.append(str(new_sink))
        possible_sinks.remove(new_sink)

    return sources, sinks


# TODO: will need to look at this again when putting more complex events back in


def populate_historical_event(
    event_type,
    num_pops,
    source,
    sink,
    migrants,
    new_deme_size,
    growth_rate,
    mig_mat_index,
):
    return " ".join(
        [
            f"{event_type}{source}{sink}",
            str(num_pops) if source == "G" else source,
            str(num_pops) if sink == "G" else sink,
            str(migrants),
            str(new_deme_size),
            str(growth_rate),
            str(mig_mat_index),
        ]
    )


def get_divergence_events(ghost_present, number_of_populations, pops_should_migrate):
    def get_deme(source_or_sink):
        if str(source_or_sink) == "G":
            return str(number_of_populations - 1)
        else:
            return str(source_or_sink)
        
    divergence_events = []
    nodes = list(range(number_of_populations))

    if ghost_present:
        nodes.pop(-1)

    number_of_sinks = (
        random.choice(range(1, number_of_populations))
        if ghost_present
        else random.choice(range(1, number_of_populations + 1))
    )
    sinks = random.sample(nodes, number_of_sinks)
    sources = [node for node in nodes if node not in sinks]

    if ghost_present:
        if random.choice([True, False]):
            sources.append("G")
        else:
            sinks.append("G")

    # the first divergence event should be in mig mat 1 
    current_migration_matrix = 1 if pops_should_migrate else 0

    while sources or len(sinks) > 1:
        current_event = []
        cur_source = random.choice(sources) if sources else random.choice(sinks)
        sources.remove(cur_source) if sources else sinks.remove(cur_source)
        cur_sink = random.choice(sinks)
        new_deme_size = random.choice([f"RELANC{cur_source}{cur_sink}", "1"])
        current_event.extend(
            [
                f"TDIV{cur_source}{cur_sink}",
                get_deme(cur_source),
                get_deme(cur_sink),
                "1",
                new_deme_size,
                "0",
                str(current_migration_matrix),
            ]
        )
        divergence_events.append(" ".join(current_event))
        if pops_should_migrate:
            current_migration_matrix += 1

    return divergence_events


# TODO: will need to look at this again when putting more complex events back in
def get_historical_event(
    event_type, ghost_present, number_of_populations, pops_should_migrate, migrants="0"
):
    sources, sinks = get_sources_and_sinks(ghost_present, number_of_populations)
    migration_matrix_index = len(sinks)  # TODO: look at this, can't get a good matrix until this is fixed
    growth_rate = 0
    new_deme_size = 0

    source = random.choice(sources)
    sink = random.choice(sinks)

    historical_event = []

    historical_event.append(
        populate_historical_event(
            event_type,
            number_of_populations,
            source,
            sink,
            migrants,
            new_deme_size,
            growth_rate,
            migration_matrix_index if pops_should_migrate else 0,
        )
    )
    return historical_event


def get_matrix_template(num_pops, ghost_present):
    matrix_label = "//Migration matrix 0"
    matrix = [matrix_label]

    for i in range(1, num_pops + 1):
        row = []
        for j in range(1, num_pops + 1):
            if i == j:
                matrix_i_j = "0.000"
            else:
                populations_list = get_population_list(num_pops, ghost_present)
                from_pop = populations_list[i - 1]
                to_pop = populations_list[j - 1]
                matrix_i_j = f"MIG{from_pop}{to_pop}"
            row.append(matrix_i_j)
        matrix.append(" ".join(row))
    return matrix


def get_migration_matrices(num_pops, ghost_present, divergence_events):
    matrices = []
    # the first matrix is a complete migration matrix
    first_matrix = get_matrix_template(num_pops, ghost_present)
    matrices.append(first_matrix)

    def extract_coalescing_population(event):
        # find the coalescing pop (the source)
        match = re.search(r"^TDIV([0-9a-zA-Z])+[0-9a-zA-Z]\s", event)
        if match:
            coalescing_population = match.group(1)
            # if ghost, replace number with "G"
            if ghost_present:
                if coalescing_population == str(num_pops - 1):
                    return "G"
            return coalescing_population
        else:
            return None

    # start with the fully filled out migration matrix
    current_matrix = get_matrix_template(num_pops, ghost_present)
    
    # loop through all divergence events going back in time
    for i in range(len(divergence_events)): 
        current_event = divergence_events[i]
        # find the migration matrix of the current event
        current_event_matrix_index = re.search(r"\d+$", current_event).group()
        # get the coalescing population (the source)
        coalescing_population = extract_coalescing_population(current_event)
        coalescing_population_in_matrix_pattern = (
            r"MIG{}[0-9a-zA-Z]*|MIG[0-9a-zA-Z]*{}".format(
                coalescing_population, coalescing_population
            )
        )

        # make a temp matrix without the label
        matrix_without_label = current_matrix[1:]

        # replace any MIG param that has the coalescing population in it
        current_matrix = [
            re.sub(coalescing_population_in_matrix_pattern, "0.000", line)
            for line in matrix_without_label
        ]
        # get updated matrix label
        matrix_label = f"//Migration matrix {current_event_matrix_index}"

        # add label to new matrix
        current_matrix.insert(0, matrix_label)    
        
        # add to the matrices list
        matrices.append(current_matrix)

    return matrices


def generate_random_params(
    tpl_filename, user_given_number_of_populations, user_given_sample_sizes
):
    # Step 1 ✓
    # determine if there is a ghost population
    add_ghost = random.choice([True, False])
    # Determine total number of populations -- either given by user or + 1 if there is a ghost pop)
    number_of_populations = (
        user_given_number_of_populations + 1
        if add_ghost
        else user_given_number_of_populations
    )

    # Step 2 ✓
    sample_sizes = (
        user_given_sample_sizes + [0] if add_ghost else user_given_sample_sizes
    )

    # Step 3 ✓
    initial_growth_rates = [0] * number_of_populations

    # Step 4 -- got something. TODO: come back and make sure this is what we want
    # determine if they're should be migration
    pops_should_migrate = random.choice([True, False])
    historical_events = []

    # get divergence events
    divergence_events = get_divergence_events(
        ghost_present=add_ghost,
        number_of_populations=number_of_populations,
        pops_should_migrate=pops_should_migrate,
    )
    historical_events.extend(divergence_events)

    # randomize adding admixture
    # TODO: randomize how many events
    # TODO: uncomment
    # if random.choice([True, False]):
    #     admixture_events = get_historical_event(
    #         event_type="TADMIX",
    #         ghost_present=add_ghost,
    #         number_of_populations=number_of_populations,
    #         migrants=random.uniform(0, 1),
    #         pops_should_migrate=pops_should_migrate
    #     )
    #     historical_events.extend(admixture_events)

    # TODO: add bottlenecks, exponential growths.

    # Step 5: build migration matrices (if there is migration) ✓
    if pops_should_migrate:
        migration_matrices = get_migration_matrices(
            num_pops=number_of_populations,
            ghost_present=add_ghost,
            divergence_events=divergence_events,
        )
    else:
        migration_matrices = []

    # Step 6 ✓
    population_effective_sizes = get_population_effective_sizes(
        number_of_populations, add_ghost
    )

    write_tpl(
        filename=tpl_filename,
        number_of_populations=number_of_populations,
        population_effective_sizes=population_effective_sizes,
        sample_sizes=sample_sizes,
        growth_rates=initial_growth_rates,
        migration_matrices=migration_matrices,
        historical_events=historical_events,
    )
