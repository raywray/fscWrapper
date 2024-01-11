NUM_OF_GROUPS=1
TDIV=0
TPLUS01=0
SAMPLE_SIZES=[1]
MUT_RATE=6e-8

def write_est_file(file_name, simple_params, complex_params):
    with open(file_name,"w") as fout:
        lines=["// Priors and rules file",
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
        fout.writelines('\n'.join(lines))

def write_tpl_file(file_name, num_pops, Ne, sample_sizes, growth_rates, mig_info, historical_events):
    with open("test1.tpl","w") as fout:
        lines=["//Number of population samples (demes)",
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
               "FREQ 1 0 MUTRATE OUTEXP"]
        fout.writelines('\n'.join(lines))
        
    


if NUM_OF_GROUPS==1:
    # NUM_OF_TOPOLOGIES=1
    write_est_file("test1.est","0","0")
    write_tpl_file("test2.tpl","0","0","0","0","0","0")

