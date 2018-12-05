#!/usr/bin/env python3

#Written by Sian Bray on 15th November 2018
#Reads through .fai (index file for a .fasta) and breaks it into a list of intervals of ~the same size.
#Each interval takes up one line in the output file and can be input directly into a GATK command (or wrapper).
#For example: line 1 could read: '-L scaffold_1 -L scaffold_2 -L scaffold_3' line 2 could read: '-L scaffold_3 -Lscaffold_4' etc).
#This script is most useful for fragmented reference genomes with 100's or 1000's of scaffolds.

#Members/friends of the Yant lab: the output of this script can be used in conjunction with a modified V3 wrapper, using eaach line as input for -scaf (you will have to change how V3 uses the -scaf input, or you can get my modified wrapper from me).

import os, sys, argparse, subprocess

parser = argparse.ArgumentParser(description='Creates an interval list for parrallelizing')
parser.add_argument('-ref', type=str, metavar='reference_fai_path', required=True, help='Path to the reference .fai index file')
parser.add_argument('-size', type=int, metavar='interval_size', default='28000000', help='Size of the interval. Default = 28 Mbp i.e. ~>1/8th of the Cochlearia reference genome')
parser.add_argument('-out', type=str, metavar='output_directory', required=True, help='Output file name. The file will be created in the directory you are in.')
args = parser.parse_args()

#create output file
output_file=open(args.out, 'w+')

print('Output file created')

#calculate number of scaffolds
input_file=open(args.ref, 'r')
scaffolds_number= len(input_file.readlines())
input_file.close
input_file=open(args.ref, 'r')

print(str(scaffolds_number)+' scaffolds found.')

#while loop to add scaffolds to line in the output
count=0
large_interval=0
small_interval=0

while scaffolds_number > count:
	current_size=0
	while current_size < args.size:
		if scaffolds_number==count:
			break
		current_line=input_file.readline()
		split_line=current_line.split('\t')
		output_file.write(' -L '+split_line[0])
		current_size+=int(split_line[1])
		count+=1
		if scaffolds_number==count:
			break
		if current_size >= args.size:
			output_file.write('\n')
			if current_size>large_interval:
				large_interval=current_size
			if small_interval==0:
				small_interval=current_size
			if small_interval>0:
				if small_interval>current_size:
					small_interval=current_size

output_file.close()
output_file=open(args.out, 'r')
output_intervals=len(output_file.readlines())

print(str(output_intervals)+' intervals determined.')
print('Largest interval is '+str(large_interval)+' bp')
print('Smallest interval is '+str(small_interval)+' bp')
