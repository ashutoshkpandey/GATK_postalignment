import os, glob
import sys,re,fileinput

Argument = []
Argument = sys.argv[1:] 

if (len(Argument)) < 4:	
	print "Usage: Input_directory Job_Script_directory Output_directory Reference_fasta" 
	sys.exit()
  
dpath = Argument[0]
Listoffile = []

def dir(patharray):
    Listdir = []
    for infile in patharray:
        Listdir.append(os.path.join(dpath,infile))
    return Listdir    

Listoffile = dir(os.listdir(dpath))
#print Listoffile

BAM = {}

for file in Listoffile:
	if file.endswith(".bam") and not os.path.getsize(file) == 0:
		if file not in BAM:
			BAM[file] = file.split("/")[-1].rstrip(".bam")

#print BAM
									
if not os.path.exists(str(Argument[1])):
	os.makedirs(str(Argument[1]))

if not os.path.exists(str(Argument[2])):
        os.makedirs(str(Argument[2]))

for file in BAM:

	jobname = ""
	jobname = str(Argument[1])+"/"+str(BAM[file])+".sh"
	
	jobfile = open(str(jobname),"w")

	jobfile.write("#!/bin/bash\n#PBS -l walltime=480:00:00\n#PBS -l nodes=1:ppn=16\n#PBS -N Base_Recalibrator_First_"+str(BAM[file])+"\n\njava -jar -Xmx40g /home/apandey/bio/GenomeAnalysisTK-2.1-9-gb90951c/GenomeAnalysisTK.jar  -T BaseRecalibrator -S LENIENT  -bfh 4000 -rbs 2000000 -I "+str(file)+" -R "+str(Argument[3])+" -o "+str(Argument[2])+"/"+str(BAM[file])+".grp   -knownSites /home/apandey/mm10_Indels_17strains.vcf -knownSites /home/apandey/mm10_snps_17strains_sort.vcf \n")

#\njava -jar -Xmx40g /home/apandey/bio/GenomeAnalysisTK-2.1-9-gb90951c/GenomeAnalysisTK.jar  -T IndelRealigner -S LENIENT -nt 16 -bfh 4000 -rbs 2000000 -I "+str(file)+" -R "+str(Argument[3])+" -targetIntervals "+str(Argument[2])+"/"+str(BAM[file])+".intervals -o "+str(Argument[2])+"/"+str(BAM[file])+".bam\n")	
	
	jobfile.close()
	
	print "qsub "+str(jobname)
	os.system("qsub "+str(jobname))
