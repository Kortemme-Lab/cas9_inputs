
#!/usr/bin/bash
#$ -N fragment_generation
#$ -o /netapp/home/rpac/crispr_cas/data/fragments
#$ -e /netapp/home/rpac/crispr_cas/data/fragments
#$ -cwd
#$ -r y
#$ -l mem_free=2G
#$ -l arch=linux-x64
#$ -l scratch=1G
#$ -l h_rt=10:00:00
#$ -q lab.q

python python_script.py

