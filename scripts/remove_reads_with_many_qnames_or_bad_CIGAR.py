#!/usr/bin/env python

import sys, argparse, pysam, gzip

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-bamin',  '--bam-file-in',  type=str,   help='BAM files sorted by qname', required=True)
parser.add_argument('-bamout', '--bam-file-out', type=str,   help='Tumor BAM File', required=True)

args     = parser.parse_args()
bam_file = args.bam_file_in
bam_out  = args.bam_file_out

with pysam.AlignmentFile(bam_file) as bam_in, pysam.AlignmentFile(bam_out, 'wb', template=bam_in) as bam_out:
    
    qnames = []
    reads  = []
    
    for bam_line in bam_in:
        
        # New qname:
        if qnames == []:
            
            qnames.append( bam_line.qname )
            reads.append( bam_line )
        
        # Already saw this qname before
        elif qnames[-1] == bam_line.qname:
            
            qnames.append( bam_line.qname )
            reads.append( bam_line )
        
        # The next qname
        elif qnames[-1] != bam_line.qname:
            
            
            if len(reads)==2:
                
                if reads[0].cigartuples:
                    cigar_length_1 = 0
                    for i in reads[0].cigartuples:
                        if i[0] == 0 or i[0] == 1 or i[0] == 4 or i[0] == 7 or i[0] == 8:
                            cigar_length_1 = cigar_length_1 + i[1]
                    qlen_1 = len( reads[0].seq )
                else:
                    cigar_length_1 = qlen_1 = None

                if reads[1].cigartuples:
                    cigar_length_2 = 0
                    for i in reads[1].cigartuples:
                        if i[0] == 0 or i[0] == 1 or i[0] == 4 or i[0] == 7 or i[0] == 8:
                            cigar_length_2 = cigar_length_2 + i[1]
                    qlen_2 = len( reads[1].seq )
                else:
                    cigar_length_2 = qlen_2 = None

                if cigar_length_1 == qlen_1 and cigar_length_2 == qlen_2:
                    [bam_out.write(read_i) for read_i in reads]
                else:
                    print(reads[0])
                    print(reads[1])
            
            qnames = []
            reads = []
            qnames.append( bam_line.qname )
            reads.append( bam_line )
            
