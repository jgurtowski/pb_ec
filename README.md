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
  4. Concatenate the output (*.corrected) files
  5. Assemble concatenated reads using Celera or another Overlap Assembler.


Example
=====

To run the example:  
  
$> cd test  
$> ../correct.sh pbread.test.fa  
  
A file pbread.test.fa.corrected will be produced. The pipeline is using the short-read 
unitigs in test/utg.test.fa for correction. If you blast both
the pbread.test.fa (uncorrected read) and pbread.test.fa.corrected to the
Oryza Sativa genome you will find that the uncorrected read has ~85% identity
while the corrected read has >99% identity.

Running on a Cluster
=====
	
	1.a Build unitigs with Celera or another assembler. Refer to chosen assembler's manual for details

	1.b Begin by splitting the Pacbio reads into bins using the partition.py script. It is suggested that
	you put anywhere between 5 and 50 pacbio reads in a file, depending on how much data you have.

	2.Edit the correct.sh script to point to the unitigs created in 1.a and set the path to the correct.py
	script.

	3. The partition.py script will have created many directories with files in them in the form 0001/p0001,
	0001/p0002 etc. To launch the correction with SGE on a particular bin cd into the bin and run:
	
	$> qsub -cwd -t 1:${FILES_PER_BIN} ../correct.sh
	
	where ${FILES_PER_BIN} is how many files per bin you gave as a parameter to the partition.py script.

	4. Wait
	
	5. Concatenate all files. Usually can do something like this from the top level dir:
	
	$> cat `find . | grep corrected$` > corrected.fa

	6. Launch your favorate overlap assembler on corrected.fa


Checking Results
=====

Internally, corrected reads are generally blasted against a reference genome to determine
their percent identity. If a reference does not exist, using blast to align directly to
unitigs or a draft assembly is another option.
