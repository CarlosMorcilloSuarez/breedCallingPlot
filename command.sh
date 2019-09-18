#!/bin/bash

INPUTFILES='./data/500_greyhound03_01.calls
./data/500_greyhound03_02.calls'
#./data/500_greyhound03_03.calls
OUTPUTFILE='./output/colors.png'
LEGEND='greyhound03 - 2 simulations 0.5x GE: 0.001 / RD: 1'
CHROMOSOME='NC_006619.3 (500 first markers)'
BREEDS='./data/all.breeds'
COLORS='./data/RedBlueYellow.colors'


python3 breedCallingPlot.py \
  --output ${OUTPUTFILE} \
  --legend "${LEGEND}" \
  --breeds ${BREEDS} \
  --colors ${COLORS} \
  --chromosome "${CHROMOSOME}" \
  ${INPUTFILES}
