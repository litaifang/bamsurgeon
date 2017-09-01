#!/usr/bin/env python

# modified by Li Tai to take proportions for pick1

import pysam
import random
import argparse
import sys
from re import sub
from collections import defaultdict as dd

def split(inbamfn, keep_secondary=False, keep_supplementary=False, seed=None, proportion=0.5):

    if seed is not None:
        random.seed(seed)

    else:
        seed = int(random.random()*1000)
        print "using seed: %d" % seed
        random.seed(seed)


    assert inbamfn.endswith('.bam')
    outbam1fn = sub('.bam$', '.pick1.bam', inbamfn)
    outbam2fn = sub('.bam$', '.pick2.bam', inbamfn)

    inbam = pysam.Samfile(inbamfn, 'rb')
    outbam1 = pysam.Samfile(outbam1fn, 'wb', template=inbam)
    outbam2 = pysam.Samfile(outbam2fn, 'wb', template=inbam)

    lastread = None

    reads = dd(list) 

    skip_secondary = 0
    skip_supplementary = 0

    for read in inbam.fetch(until_eof=True):
        if (read.is_secondary and args.secondary) or (read.is_supplementary and args.supplementary) or (not read.is_supplementary and not read.is_secondary):
            if lastread is not None and read.qname == lastread.qname:
                reads[read.qname].append(read)

            else:
                if lastread is not None:
                    ob = None
                    if random.random() < proportion:
                        ob = outbam1
                    else:
                        ob = outbam2

                    for outread in reads[lastread.qname]:
                        ob.write(outread)

                    del reads[lastread.qname]
                reads[read.qname].append(read)
            lastread = read
        elif read.is_secondary:
            skip_secondary += 1
        else:
            skip_supplementary +=1


    ob = None
    if random.random() > 0.5:
        ob = outbam1
    else:
        ob = outbam2

    for read in reads[lastread.qname]:
        ob.write(read)

    outbam1.close()
    outbam2.close()
    inbam.close()

    if not args.secondary and skip_secondary >= 1:
        print "skipped %d secondary reads" % skip_secondary

    if not args.supplementary and skip_supplementary >= 1:
        print "skipped %d supplementary reads" % skip_supplementary

def main(args):
    split(args.bam, keep_secondary=args.secondary, keep_supplementary=args.supplementary,seed=args.seed, proportion=args.proportion)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='split one bam into two')
    parser.add_argument('-b', '--bam', required=True, help='input BAM: must be sorted by readname (e.g. samtools sort -n)')
    parser.add_argument('--secondary', default=False, action='store_true', help='keep secondary alignments')
    parser.add_argument('--supplementary', default=False, action='store_true', help='keep supplementary alignments')
    parser.add_argument('--seed', default=None, help='set PRNG seed')
    parser.add_argument('--proportion', default=0.5, type=float, help='proportion of reads going to pick1')
    args = parser.parse_args()
    main(args)
