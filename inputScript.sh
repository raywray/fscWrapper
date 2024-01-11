#!/bin/bash

# Step 1: get user input
NUM_OF_GROUPS=1
TDIV=0
TPLUS01=0
SAMPLE_SIZES=(100)
MUT_RATE=6e-8

# Step 2: determine number of topologies to create.
# if NUM_OF_GROUPS = 1, #t = 1
# if NUM_OF_GROUPS = 2, #t = 1
# if NUM_OF_GROUPS = 3, #t = 4

if [ $NUM_OF_GROUPS -eq 1 ]; then
  NUM_OF_TOPOLOGIES=1
  cd Panmixia/t1/
  cp pre_template.est t1.est
  cp pre_template.tpl t1.tpl
  sed /s/"TDIV_PLACEHOLDER"/$TDIV/ t1.est
  sed /s/"TPLUS01_PLACEHOLDER"/$TPLUS01/ t1.tpl

else
  NUM_OF_TOPOLOGIES=1
fi
echo $NUM_OF_TOPOLOGIES

# Step 3: create .tpls and .ests for each topology

# Step 4: add in migration rates for appropriate models
