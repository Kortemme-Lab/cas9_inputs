#!/usr/bin/env python2

"""\
Make copies of the given PDB files where the atom and residue numbers count 
consecutively from one.

Usage:
    renumber_residues.py [<pdbs>...] [--clean]

Options:
    -c --clean
        Remove any files in the current directory with "renumbered" in their 
        names, which are assumed to have been generated by earlier calls to 
        this script.
"""

def renumber_pdb(input_path):
    import os.path
    import yaml

    # Read the input file.

    if input_path.endswith('.gz'):
        import gzip
        open = gzip.open
    else:
        open = __builtins__.open

    with open(input_path) as file:
        input_lines = file.readlines()
    
    # Renumber all the atoms in this file.

    input_resi_before = -1
    output_resi = 0
    output_atom = 0
    output_lines = []
    resi_map = {}

    for input_line in input_lines:
        if not input_line.startswith('ATOM') and not input_line.startswith('HETATM'):
            continue

        # Update the atom and residue counters.

        output_atom += 1
        input_resi = int(input_line[22:26])
        if input_resi != input_resi_before:
            output_resi += 1
        input_resi_before = input_resi

        # Generate the renumbered line.

        output_lines.append(
                input_line[0:6] + 
                '{:5d}'.format(output_atom) + 
                input_line[11:22] +
                '{:4d}'.format(output_resi) +
                input_line[26:]
        )

        # Keep track of the mapping between input and output residue numbers.

        resi_map[input_resi] = output_resi
                
    # Write the renumbered atoms to disk.

    root, ext = os.path.splitext(input_path)
    output_path = root + '_renumbered' + ext

    with open(output_path, 'w') as file:
        file.writelines(output_lines)

    # Write the residue map to disk.

    resi_map_path = root + '_renumbered_map.yaml'
    with open(resi_map_path, 'w') as file:
        yaml.dump(resi_map, file)

if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)

    if args['--clean']:
        from subprocess import call
        call('rm -i *renumbered*', shell=True)

    for pdb in args['<pdbs>']:
        renumber_pdb(pdb)
