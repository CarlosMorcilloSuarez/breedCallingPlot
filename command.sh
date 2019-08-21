#!/bin/bash

INPUTFILES='./data/greyhound03_10.calls 
./data/greyhound03_01.calls
./data/greyhound03_02.calls
./data/greyhound03_03.calls
./data/greyhound03_04.calls
./data/greyhound03_05.calls
./data/greyhound03_06.calls
./data/greyhound03_07.calls
./data/greyhound03_08.calls
./data/greyhound03_09.calls'
OUTPUTFILE='./output/greyhound03.png'
LEGEND='greyhound03 - 10 simulations 0.5x GE: 0.001 / RD: 1'
CHROMOSOME='NC_006619.3'
BREEDS='./data/all.breeds'


python3 breedCallingPlot.py \
  --output ${OUTPUTFILE} \
  --legend "${LEGEND}" \
  --breeds ${BREEDS} \
  --chromosome ${CHROMOSOME} \
  ${INPUTFILES}


#--breeds ${BREEDS} \
