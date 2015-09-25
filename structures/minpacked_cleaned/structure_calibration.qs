
#!/bin/csh
#$ -N structure_calibration
#$ -o /netapp/home/rpac/crispr_cas/data/minpacked_cleaned/
#$ -e /netapp/home/rpac/crispr_cas/data/minpacked_cleaned/
#$ -cwd
#$ -r y
#$ -l mem_free=3G
#$ -l arch=linux-x64    
#$ -l q=lab.q
#$ -l h_rt=24:00:00
#$ -t 2

set tasks= ( 4UN3 4UN3_with_2_waters )

echo start_date:
date
hostname
echo $SGE_TASK_ID
set task=$tasks[$SGE_TASK_ID]
echo $task
echo
cd /netapp/home/rpac/crispr_cas/data/minpacked_cleaned/

/netapp/home/rpac/Rosetta_57138/main/source/bin/fixbb.linuxgccrelease -database /netapp/home/rpac/Rosetta_57138/main/database/ -s /netapp/home/rpac/crispr_cas/data/$task.pdb.gz -extra_res_fa /netapp/home/rpac/Rosetta_57138/main/database/chemical/residue_type_sets/fa_standard/residue_types/water/HOH.params -in:file:fullatom -overwrite -nstruct 1 -out:pdb_gz -out::path /netapp/home/rpac/crispr_cas/data/minpacked_cleaned// -ignore_zero_occupancy false -constant_seed -ex1 -ex2 -extrachi_cutoff 0 -flip_HNQ -no_optH false -preserve_header -min_pack -packing:repack_only

echo moving outfiles...
mv $task\_0001.pdb.gz $task\_minpacked.pdb.gz

echo
echo $SGE_TASK_ID
echo end_date:
date
