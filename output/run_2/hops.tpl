//Number of population samples (demes)
5
//Population effective sizes (number of genes)
NPOP_0
NPOP_1
NPOP_2
NPOP_3
NPOP_G
//Sample sizes
2
4
6
12
0
//Growth rates : negative growth implies population expansion
0
0
0
0
0
//Number of migration matrices : 0 implies no migration between demes
4
//Migration matrix 0
0.000 MIG_1to0 MIG_2to0 MIG_3to0 MIG_Gto0
MIG_0to1 0.000 MIG_2to1 MIG_3to1 MIG_Gto1
MIG_0to2 MIG_1to2 0.000 MIG_3to2 MIG_Gto2
MIG_0to3 MIG_1to3 MIG_2to3 0.000 MIG_Gto3
MIG_0toG MIG_1toG MIG_2toG MIG_3toG 0.000
//Migration matrix 1
0.000 MIG_1to0 MIG_2to0 MIG_3to0 MIG_Gto0
MIG_0to1 0.000 MIG_2to1 MIG_3to1 MIG_Gto1
MIG_0to2 MIG_1to2 0.000 MIG_3to2 MIG_Gto2
MIG_0to3 MIG_1to3 MIG_2to3 0.000 MIG_Gto3
MIG_0toG MIG_1toG MIG_2toG MIG_3toG 0.000
//Migration matrix 2
0.000 MIG_1to0 MIG_2to0 MIG_3to0 MIG_Gto0
MIG_0to1 0.000 MIG_2to1 MIG_3to1 MIG_Gto1
MIG_0to2 MIG_1to2 0.000 MIG_3to2 MIG_Gto2
MIG_0to3 MIG_1to3 MIG_2to3 0.000 MIG_Gto3
MIG_0toG MIG_1toG MIG_2toG MIG_3toG 0.000
//Migration matrix 3
0.000 MIG_1to0 MIG_2to0 MIG_3to0 MIG_Gto0
MIG_0to1 0.000 MIG_2to1 MIG_3to1 MIG_Gto1
MIG_0to2 MIG_1to2 0.000 MIG_3to2 MIG_Gto2
MIG_0to3 MIG_1to3 MIG_2to3 0.000 MIG_Gto3
MIG_0toG MIG_1toG MIG_2toG MIG_3toG 0.000
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
3 historical events
TDIV_Gto2 2 4 1 RES_Gto2 0 1
TDIV_3to1 1 3 1 RES_3to1 0 2
TDIV_Gto0 0 4 1 RES_Gto0 0 3
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE OUTEXP