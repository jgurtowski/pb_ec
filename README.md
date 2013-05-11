Pacbio Error Correction with Mummer
=====

This is a pipeline developed around Mummer
to correct Pacbio reads using high-identity short reads


Files
=====
	
correct.sh - Runs the pipeline (local or sge)  
correct.py - Corrects pb reads given output from 'show-snps'  
partition.py - Convenience script to partition input Pacbio reads (for cluster)  

Dependencies
=====
Mummer must be installed and in your PATH. In particular the following subprograms
are required to be in your path:
  
nucmer  
delta-filter  
show-snps  


Workflow
=====

The high level workflow is as follows:
  
  1. Build Unitigs of short reads using your favorite assembler
  2. Update file paths in correct.sh
  3. If running on a cluster, partition pacbio reads using partition.py
  3. Run correct.sh locally or on a cluster
  4. Concatenate output *.corrected files
  5. Assemble concatenated *.corrected reads using Celera or other Overlap Assembler.



Example
=====

To run the example:  
  
$> cd test  
$> ../correct.sh pbread.test.fa  
  
A file pbread.test.fa.corrected will be produced. The pipeline is using
the test/utg.test.fa as the short-unitigs for correction. You blast both
the pbread.test.fa (uncorrected read) and pbread.test.fa.corrected to the
Oryza Sativa genome and find that the uncorrected read has ~85% identity
while the corrected read has >99% identity.


Checking Results
=====

Internally, corrected reads are generally blasted against a reference genome to determine
their percent identity. If a reference does not exist, using blast to align directly to
unitigs or a draft assembly is another option.
