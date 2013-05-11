#!/usr/bin/env python

import sys
from Bio import SeqIO

if not len(sys.argv) == 3:
    print "correct.py in.fa in.snps"
    sys.exit(-1)


class SNPProducer:
    
    def __init__(self, filesnps):
        self.i = 0
        self.ia = 0
        self.snps = []
        
        for s in filesnps:
            t = (int(s[0]),s[1],s[2])
            if len(self.snps) > 0 and self.snps[-1][0][0] == t[0]:
                self.snps[-1].append(t)
            else:
                self.snps.append([t])

    def __iter__(self):
        return self

    def next(self):
        ret = None
        if self.ia >= len(self.snps):
            raise StopIteration()

        if self.i == self.snps[self.ia][0][0]:
            ret = self.snps[self.ia]
            self.ia += 1
        self.i += 1
        return ret

class SNPReader:

    def __init__(self,snpfh):
        self.snpfh = snpfh
        self.nxt_line = self.snpfh.readline().strip().split()

    def __iter__(self):
        return self

    def next(self):

        if self.nxt_line == None:
            raise StopIteration()

        arr = [self.nxt_line]
        
        while True:
            line = self.snpfh.readline()
            if not line:
                self.nxt_line = None
                break
            a = line.strip().split()
            if a[16] == arr[-1][16]:
                arr.append(a)
            else:
                self.nxt_line = a
                break

        return arr
        
def correct(pileup):
    #Actually do the correction
    corrected = ""
    pileupstr = ""
    j =0
    for entry in pileup:
        pileupstr += str(j) + " " +str(entry) +" "
        if entry[1] == None: 
            if not entry[0] == " ": #match
                corrected += entry[0]
                pileupstr += "add match: %s\n" % entry[0]
        elif entry[1][0][1] == '.': #insertion
            if entry[0] != " ": #if we're not at the start
                corrected += entry[0] #add the current char
                pileupstr += "add current: %s " % entry[0]
            for insert in entry[1]:
                corrected += insert[2] #add insertion
            pileupstr += "added insertions\n"
        elif not entry[1][0][2] == '.': #not deletion, so mismatch
            corrected += entry[1][0][2]
            pileupstr += "added mismatch %s\n" % entry[1][0][2]
        else:
            pileupstr += "deleted %s \n" % entry[0]
        #else we have a deletion, don't add that base
        j += 1
    return (corrected,pileupstr)

    

def main():

    ffh = open(sys.argv[1]) #uncorrected entries in fasta
    sfh = open(sys.argv[2]) #snps called by show-snps
    snpReader = SNPReader(sfh)
    uncorrected_seqs = {}
    #read in all uncorrected sequences b/c nucmer doesn't output
    #snps in the same order
    for fasta_entry in SeqIO.parse(ffh, "fasta"):
        name = str(fasta_entry.name)
        uncorrected_seqs[name] = str(fasta_entry.seq)
    
    for snpArray in snpReader:
        readname = snpArray[0][16]
        if not uncorrected_seqs.has_key(readname):
            raise Exception("Cannot find %s from snps file in input reads" % readname)
        seq = uncorrected_seqs[readname]
        (corrected_seq, pileup_debug) = correct(zip(list(" " + seq),SNPProducer(snpArray)))
        print ">" +readname+ "_corrected"
        print corrected_seq
        sys.stderr.write(">" + readname +"\n" )
        sys.stderr.write(pileup_debug+"\n")
        
    ffh.close()
    sfh.close()

if __name__ == "__main__":
    main()
