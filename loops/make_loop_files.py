#!/usr/bin/env python

starts = 1378, 1387, 1393
ends = 1402, 1408

for start in starts:
    for end in ends:
        loop_spec = 'LOOP {0} {1} {1} 0 1'.format(start, end)
        loop_name = '{0}_{1}.loop'.format(start, end)

        with open(loop_name, 'w') as file:
            file.write(loop_spec)


