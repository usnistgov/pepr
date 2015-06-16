#!/bin/bash
for fq in *fastq;
	do
		head -n 40000 $fq >  T$fq
	done
