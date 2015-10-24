#!/usr/bin/env python

starts = [1379, 1388, 1394]
ends = [1403, 1409]

for start in starts:
    for end in ends:
        loop_spec = '{0} {1} {1} 0 1'.format(start, end)
        loop_name = '{0}_{1}.loop'.format(start, end)

        with open(loop_name, 'w') as file:
            file.write(loop_spec)


