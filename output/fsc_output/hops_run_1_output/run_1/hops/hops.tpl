//Number of population samples (demes)
5
//Population effective sizes (number of genes)
N_POP0
N_POP1
N_POP2
N_POP3
N_POPG
//Sample Sizes
18
19
41
20
0
//Growth rates : negative growth implies population expansion
0
0
0
0
0
//Number of migration matrices : 0 implies no migration between demes
0
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
5 historical event
T_DIVG3 4 3 1 1 0 0
T_DIV01 0 1 1 RELANC01 0 0
T_ADMIX21 2 1 0.6578944426793816 1 0 0
T_DIV23 2 3 1 RELANC23 0 0
T_DIV13 1 3 1 RELANC13 0 0
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE OUTEXP