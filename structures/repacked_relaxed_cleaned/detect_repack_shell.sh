#!/bin/bash

ROSETTA_DIR=~/postdoc/Rosetta_new/main/
INPUT_PDB=$1
RESFILE=$2
WATER_PARAMS=$ROSETTA_DIR/database/chemical/residue_type_sets/fa_standard/residue_types/water/HOH.params

$ROSETTA_DIR/source/bin/create_clash-based_repack_shell.macosclangrelease -database $ROSETTA_DIR/database -s $INPUT_PDB -resfile $RESFILE -extra_res_fa $WATER_PARAMS -ex1 -ex2 -extrachi_cutoff 0 