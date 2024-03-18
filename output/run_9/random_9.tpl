//Number of population samples (demes)
4
//Population effective sizes (number of genes)
NPOP_0
NPOP_1
NPOP_2
NPOP_G
//Sample sizes
2
4
4
0
//Growth rates : negative growth implies population expansion
0
0
0
0
//Number of migration matrices : 0 implies no migration between demes
3
//Migration matrix 0
0.000 MIG_1to0 MIG_2to0 MIG_Gto0
MIG_0to1 0.000 MIG_2to1 MIG_Gto1
MIG_0to2 MIG_1to2 0.000 MIG_Gto2
MIG_0toG MIG_1toG MIG_2toG 0.000
//Migration matrix 1
0.000 MIG_1to0 MIG_2to0 MIG_Gto0
MIG_0to1 0.000 MIG_2to1 MIG_Gto1
MIG_0to2 MIG_1to2 0.000 MIG_Gto2
MIG_0toG MIG_1toG MIG_2toG 0.000
//Migration matrix 2
0.000 MIG_1to0 MIG_2to0 MIG_Gto0
MIG_0to1 0.000 MIG_2to1 MIG_Gto1
MIG_0to2 MIG_1to2 0.000 MIG_Gto2
MIG_0toG MIG_1toG MIG_2toG 0.000
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
2 historical events
TDIV_2to0 0 2 1 RES_2to0 0 1
TDIV_Gto1 1 3 1 RES_Gto1 0 2
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE OUTEXP