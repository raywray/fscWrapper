//Number of population samples (demes)
3
//Population effective sizes (number of genes)
NPOP_0
NPOP_1
NPOP_2
//Sample sizes
2
4
6
//Growth rates : negative growth implies population expansion
0
0
0
//Number of migration matrices : 0 implies no migration between demes
3
//Migration matrix 0
0.000 MIG_1to0 MIG_2to0
MIG_0to1 0.000 MIG_2to1
MIG_0to2 MIG_1to2 0.000
//Migration matrix 1
0.000 MIG_1to0 MIG_2to0
MIG_0to1 0.000 MIG_2to1
MIG_0to2 MIG_1to2 0.000
//Migration matrix 2
0 0 0
0 0 0
0 0 0
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
3 historical events
TAdm_2to1 1 2 a_2to1 1 0 0 TAdm_1to2 2 1 a_1to2 1 0 0 
TDIV_2to1 1 2 1 RES_2to1 0 1
TDIV_2to0 0 2 1 RES_2to0 0 2
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE OUTEXP