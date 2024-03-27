//Number of population samples (demes)
4
//Population effective sizes (number of genes)
NPOP_0
NPOP_1
NPOP_2
NPOP_3
//Sample sizes
2
4
6
12
//Growth rates : negative growth implies population expansion
GrowthP0
GrowthP1
GrowthP2
GrowthP3
//Number of migration matrices : 0 implies no migration between demes
4
//Migration matrix 0
0.000 MIG_1to0 MIG_2to0 MIG_3to0
MIG_0to1 0.000 MIG_2to1 MIG_3to1
MIG_0to2 MIG_1to2 0.000 MIG_3to2
MIG_0to3 MIG_1to3 MIG_2to3 0.000
//Migration matrix 1
0.000 MIG_1to0 MIG_2to0 MIG_3to0
MIG_0to1 0.000 MIG_2to1 MIG_3to1
MIG_0to2 MIG_1to2 0.000 MIG_3to2
MIG_0to3 MIG_1to3 MIG_2to3 0.000
//Migration matrix 2
0.000 MIG_1to0 MIG_2to0 MIG_3to0
MIG_0to1 0.000 MIG_2to1 MIG_3to1
MIG_0to2 MIG_1to2 0.000 MIG_3to2
MIG_0to3 MIG_1to3 MIG_2to3 0.000
//Migration matrix 3
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
5 historical events
TAdm_1to2 2 1 a_1to2 1 0 0 TAdm_2to1 1 2 a_2to1 1 0 0 
TAdm_0to3 3 0 a_0to3 1 0 0 TAdm_3to0 0 3 a_3to0 1 0 0 
TDIV_3to1 1 3 1 RES_3to1 0 1
TDIV_3to2 2 3 1 RES_3to2 0 2
TDIV_3to0 0 3 1 RES_3to0 0 3
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE OUTEXP