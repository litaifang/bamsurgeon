#!/usr/bin/env python

import pysam
import sys


def markreads(bamfn, outfn):
    bam = pysam.AlignmentFile(bamfn, 'rb')
    out = pysam.AlignmentFile(outfn, 'wb', template=bam)

    for read in bam.fetch(until_eof=True):
        tags = read.tags
        tags.append(('BS',1))
        read.tags = tags
        out.write(read)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        markreads(*sys.argv[1:])

    else:
        print 'usage:', sys.argv[0], '<input BAM> <output BAM>'
            
