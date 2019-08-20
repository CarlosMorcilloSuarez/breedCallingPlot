#!/bin/bash

INPUTFILES='./data/mixed_001_R_1.out'
OUTPUTFILE='./output/mixed_001_R_1.png'
LEGEND='mixed GE: 0.001 / RD: 1'
CHROMOSOME='NC_006620.3'
BREEDS='./data/all.breeds'


python3 breedCallingPlot.py \
  --output ${OUTPUTFILE} \
  --legend "${LEGEND}" \
  --breeds ${BREEDS} \
  --chromosome ${CHROMOSOME} \
  "${INPUTFILE}"


#--input "${INPUTFILE}" \ 
#--input <(cat "${INPUTFILE}" | head -1000) \
