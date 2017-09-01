#!/usr/bin/env python
# Split sorted BAM files into two BAM files

import pysam, random, argparse, sys
from re import sub
from copy import copy

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-b',      '--bam',        type=str,   help='BAM files sorted by qname', required=True)
parser.add_argument('-pick1',  '--pick1',      type=str,   help='pick 1 filename', required=False, default=None)
parser.add_argument('-pick2',  '--pick2',      type=str,   help='pick 2 filename', required=False, default=None)
parser.add_argument('-sm1',    '--pick1-sample-name', type=str, default='pick1', help='pick1 sample name tag')
parser.add_argument('-sm2',    '--pick2-sample-name', type=str, default='pick2', help='pick2 sample name tag')
parser.add_argument('-seed',   '--seed',       type=int,  default=None, help='set PRNG seed')
parser.add_argument('-prop',   '--proportion', type=float, default=0.5, help='proportion of reads going to pick1')
parser.add_argument('-down',   '--downsample', type=float, default=1, help='downsample to this fraction')
parser.add_argument('--secondary', default=False, action='store_true', help='keep secondary alignments')
parser.add_argument('--supplementary', default=False, action='store_true', help='keep supplementary alignments')

args    = parser.parse_args()

seed    = args.seed
prop    = args.proportion
down    = args.downsample

inbamfn = args.bam
pick1fn = args.pick1 if args.pick1 else sub('.bam$', '.pick1.bam', inbamfn)
pick2fn = args.pick2 if args.pick2 else sub('.bam$', '.pick2.bam', inbamfn)
sm1     = args.pick1_sample_name
sm2     = args.pick2_sample_name

keep_secondary = args.secondary
keep_supplementary = args.supplementary

if seed is not None:
    random.seed(seed)
else:
    seed = int(random.random()*1000)
    print "using seed: %d" % seed
    random.seed(seed)


def keep_read(secondary, supplementary, is_secondary, is_supplementary):
    
    if not (is_secondary or is_supplementary):
        return True
    elif (is_secondary) and (secondary is True):
        return True
    elif (is_supplementary) and (supplementary is True):
        return True
    else:
        False
    

with pysam.AlignmentFile(inbamfn) as inbam:
    
    pick1_header = copy( inbam.header )
    pick2_header = copy( inbam.header )

    for rg_i in pick1_header['RG']:
        rg_i['SM'] = sm1

    for rg_i in pick2_header['RG']:
        rg_i['SM'] = sm2


with pysam.AlignmentFile(inbamfn) as inbam, \
pysam.AlignmentFile(pick1fn, 'wb', header=pick1_header) as pick1, \
pysam.AlignmentFile(pick2fn, 'wb', header=pick2_header) as pick2:
    
    outBams = [pick1, pick2]
    qname_at = {} # 1 for pick1, 2 for pick2, None for OuttaHere
    
    for bam_i in inbam:
        
        if keep_read(keep_secondary, keep_supplementary, bam_i.is_secondary, bam_i.is_supplementary):
        
            # This read name bas been seen before, and already desiganted 1 (pick1), 2 (pick2), or None (gone'r)
            if bam_i.qname in qname_at:
                
                if qname_at[bam_i.qname] == 1:
                    pick1.write( bam_i )
                    
                elif qname_at[bam_i.qname] == 2:
                    pick2.write( bam_i )
                    
                # After seeing the same qname, delete it regardless what
                del qname_at[bam_i.qname]
            
            # If this read name is seen for the first time, does it get thrown out due to down-sampling?
            elif random.random() <= down:
                
                assert bam_i.qname not in qname_at
                
                if random.random() < prop:
                    pick1.write( bam_i )
                    qname_at[ bam_i.qname ] = 1
                    
                else:
                    pick2.write( bam_i )
                    qname_at[ bam_i.qname ] = 2
            
            # Thrown out due to down-sampling
            else:
                qname_at[ bam_i.qname ] = None
                
        else:
            qname_at[ bam_i.qname ] = None
    
