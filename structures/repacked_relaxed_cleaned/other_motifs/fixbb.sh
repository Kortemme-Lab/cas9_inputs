#!/usr/bin/env sh

rosetta="$HOME/rosetta/crispr"
fixbb="$rosetta/source/bin/fixbb"

$fixbb                                                              \
    -database "$rosetta/database"                                   \
    -in:file:s "../other_bases/4UN3_calibrated_AA.pdb.gz"           \
    -out:pdb_gz                                                     \
    -nstruct 1                                                      \
    -resfile "qq.resfile"                                           \
    -ex1 -ex2 -extrachi_cutoff 0                                    \
    -overwrite                                                      \

rm score.sc
mv 4UN3_calibrated_AA_0001.pdb.gz 4UN3_calibrated_AA_QQ.pdb.gz
