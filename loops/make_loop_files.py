#!/usr/bin/env python

starts = [1339, 1348, 1354]
ends = [1363, 1369]

for start in starts:
    for end in ends:
        loop_spec = 'LOOP {0} {1} {1} 0 1'.format(start, end)
        loop_name = '{0}_{1}.loop'.format(start, end)

        with open(loop_name, 'w') as file:
            file.write(loop_spec)


