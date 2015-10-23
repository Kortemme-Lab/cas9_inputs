import sys
from sys import argv
from Bio.PDB import *

parser = PDBParser()

pdb_name = argv[1]

i = 1
j = 1
out_file = open(pdb_name.rstrip('.pdb')+"_renum.pdb", 'w')
structure = open(pdb_name)
for line in structure:
	if j == 1:
		current_residue = line[22:26]
	if line[22:26] != current_residue:
		i+=1
		current_residue = line[22:26]
	if line[0:4] == "ATOM" or line[0:6] == "HETATM":
		if i < 10:
			editline = "%s   %s%s" % (line[0:22], i, line[26:])
		elif i >= 10 and i < 100:
			editline = "%s  %s%s" % (line[0:22], i, line[26:])
		elif i >= 100 and i < 1000:
			editline = "%s %s%s" % (line[0:22], i, line[26:])
		else:
			editline = "%s%s%s" % (line[0:22], i, line[26:])
		out_file.writelines(editline)
		j+=1
out_file.close()