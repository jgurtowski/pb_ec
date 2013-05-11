#!/bin/bash -x

set -e 

source ~/.bashrc

CORRECT_SCRIPT=$(dirname "${BASH_SOURCE[0]}")/correct.py
UNITIG_FILE=$(dirname "${BASH_SOURCE[0]}")/test/utg.test.fa

if [ -z "$1" ]
    then
    echo "correct.sh prefix Missing prefix"
    exit -1
fi

FILE=$1
if [[ $SGE_TASK_ID ]]
    then
    suffix=`printf "%04d" $SGE_TASK_ID`
    FILE=${FILE}${suffix}
fi

nucmer --maxmatch -l 11 --nooptimize -p ${FILE} ${FILE} ${UNITIG_FILE}

delta-filter -o 40 -i 70.0 -r ${FILE}.delta > ${FILE}.delta.r

show-snps -H -l -r ${FILE}.delta.r > ${FILE}.snps

python ${CORRECT_SCRIPT} ${FILE} ${FILE}.snps > ${FILE}.corrected 2> ${FILE}.pileup

