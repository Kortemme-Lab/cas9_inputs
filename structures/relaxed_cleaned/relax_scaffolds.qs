
#!/bin/csh
#$ -N relax_scaffolds
#$ -o /netapp/home/rpac/crispr_cas/data/relaxed_cleaned/
#$ -e /netapp/home/rpac/crispr_cas/data/relaxed_cleaned/
#$ -cwd
#$ -r y
#$ -l mem_free=3G
#$ -l arch=linux-x64    
#$ -l q=lab.q
#$ -l h_rt=24:00:00
#$ -t 2

set tasks= ( 4UN3.pdb.gz 4UN3_with_2_waters.pdb.gz )

set outfile_names= ( 4UN3.pdb.gz4UN3_0001.pdb.gz 4UN3_with_2_waters.pdb.gz4UN3_with_2_waters_0001.pdb.gz )

echo start_date:
date
hostname
echo $SGE_TASK_ID
set task=$tasks[$SGE_TASK_ID]
echo $task
set outfile_name=$outfile_names[$SGE_TASK_ID]
echo
cd /netapp/home/rpac/crispr_cas/data/relaxed_cleaned/

/netapp/home/rpac/Rosetta_57138/main/source/bin/relax.linuxgccrelease -database /netapp/home/rpac/Rosetta_57138/main/database/ -s /netapp/home/rpac/crispr_cas/data/$task -extra_res_fa /netapp/home/rpac/Rosetta_57138/main/database/chemical/residue_type_sets/fa_standard/residue_types/water/HOH.params -out:pdb_gz -out:path /netapp/home/rpac/crispr_cas/data/relaxed_cleaned/ -out:prefix $task -ignore_zero_occupancy false -constant_seed -relax:constrain_relax_to_start_coords -relax:coord_constrain_sidechains -relax:ramp_constraints false -ex1 -ex2 -extrachi_cutoff 0 -use_input_sc -flip_HNQ -no_optH false -preserve_header -relax:min_type lbfgs_armijo_nonmonotone

echo
echo renaming outfile...
mv $outfile_name $task

echo
echo $SGE_TASK_ID
echo end_date:
date

