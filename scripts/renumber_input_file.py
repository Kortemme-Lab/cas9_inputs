#!/usr/bin/env python

"""\
Search files for residue numbers and replace them according to a map.  You 
would need to do this if you had added or removed atoms from you input 
structure for some reason, and now needed to update all the resfiles, loops 
files, etc. that reference that structure.

Usage:
    ./renumber_input_file.py <resi_map> <input_files>...

Arguments:
    <resi_map>
        A JSON file mapping the old residue indices to the new ones.

    <input_file>
        Any file that may contain old residue numbers.  For each input, and 
        output with a '_renumbered' prefix will be generated.

This program works by using a regular expression to search for entirely numeric 
words.  Any words it finds that are also in the map will be replaced.  Note 
that this is pretty naive, so you wouldn't want to run this on a file with 
numbers that don't refer to residues.
"""

import os, re, json

def renumber_file(input_path, resi_map):

    # Read the input file.

    with open(input_path) as file:
        contents = file.read()

    # Search for number in the input file and update them.

    def map_number(re_match):   # (no fold)
        key = re_match.group(0)
        value = resi_map.get(key, key)
        return '{0:0{1}d}'.format(int(value), len(key))

    renumbered_contents = re.sub(
            r'[0-9]+', map_number, contents)

    # Write the output file.

    root, ext = os.path.splitext(input_path)
    output_path = root + '_renumbered' + ext

    with open(output_path, 'w') as file:
        file.write(renumbered_contents)

if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)

    # Load the residue map.

    with open(args['<resi_map>']) as file:
        resi_map = json.load(file)

    # Renumber each input file.

    for path in args['<input_files>']:
        renumber_file(path, resi_map)



