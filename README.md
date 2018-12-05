# Reference-genome-interval-determination
This script will create a list of intervals of ~ the same size from a .fai file (FASTA file index).
Each line of the output can be input directly into a GATK command. This script is especially useful for parallelizing with a highly fragmented reference genome that contains 100's or 1000's of scaffolds.
Notes on use are in the comments at the top of the file.
