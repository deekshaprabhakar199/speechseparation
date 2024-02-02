#!/bin/bash

# align-wer.sh - Shell script to take an input CSV file of the form:
#
# id|ref|hyp
# 0008d984a300e476600a2bfbe41bf|porting|forty year
# 000e153f20452a66600f4b7a6b306|upgrade uh|upgrade or
# ...
#
# and create a new csv file called '<name>-Aligned.csv',where <name> is the
# base name of the input file.  The new csv file is created by aligning 
#'ref' and 'hyp' using the sclite(1) tool. The format of the new file is 
# as follows:
#
# id|ref|hyp|wer
# 0008d984a300e476600a2bfbe41bf|***** porting |forty year|50.0
# 000e153f20452a66600f4b7a6b306|upgrade uh |upgrade or|50.0
# ...
#
# The new file can be used in subsequent alignment analysis, or it can be
# used as input to the accompanying R script which will transform it into 
# another output file that can be ingested by other RAIL programs.  Please 
# see the comment block in the R file for further processing.
#
# The new file will also have the word error rate (WER) of the ref/hyp.
#
# (C) 2021-2023 Vijay K. Gurbani <vgurbani@vailsys.com>
#
# All the places below where comments start with **** must be looked at 
# before running this shell script. (Will be good to automate this at some 
# time.)
#
# TODO: Add some error resiliency.

# **** NOTE INPUT NEEDED: Specify the two variables below.
# **** INPUT_FILE is the path/name to the CSV file to ingest.
# SCLITE_EXE is the path/name to the sclite(1) binary.
INPUT_FILE=
SCLITE_EXE=

# Create the output file.  If the input file is foo.csv, then the
# output file will be named foo-Aligned.csv.
OUTPUT_FILE=`basename ${INPUT_FILE} .csv`-Aligned.csv

/bin/rm -f $OUTPUT_FILE

# Some local error flags that are set when an error occurs.  These
# flags will cause error information to be printed when the script
# finishes.
flag_1="0"
flag_1_str=""

# **** DO NOT CHANGE the order of the columns or the column names in the 
# line below.  The R program that ingests the output from this program
# expects the header to be as shown in the line below.
echo "id|ref|hyp|wer" > $OUTPUT_FILE  # Put header in ...

if [ -f /usr/bin/dos2unix ]; then
   /usr/bin/dos2unix $INPUT_FILE
fi

# Get the first line of the input file and make sure it contains the
# expected header (see comment block at beginning).
head=$(head -n 1 ${INPUT_FILE})
id=`echo $head | cut -d'|' -f 1`
if [ ${id} != "id" ]
then
   echo "First line, first column MUST be named 'id'."
   echo "See comment block in code."
   exit 1
fi
ref=`echo $head | cut -d'|' -f 2`
hyp=`echo $head | cut -d'|' -f 3`
echo "${id}|${ref}|${hyp}|wer" > $OUTPUT_FILE  # Put header in ... and
# add the 'wer' column in the output.

# **** The default separtor in the input file is assumed to be '|'.  If 
# **** this is not the case, please change IFS below.
while IFS='|' read -r col1 col2 col3 
do   
   # *** MAKE SURE THAT THE COLUMN ORDER HERE MATCHES THE INPUT CSV FILE!!!
   # *** Which file contains the hyp and which the ref is important to the
   # *** sclite(1) command below.
   # col1 -> id   MUST BE NAMED 'id'
   # col2 -> ref  Maybe named anything, the reference string (human transcribed)
   # col3 -> hyp  Maybe named anything, the hypothesis string (ASR transcribed)

   if [[ "$col1" = "id" || "$col1" = "ID" ]]; then
      echo "First line is header, continuing..."
      continue
   fi

   # Some error checking.
   if [ "$col1" = "" ]; then
      echo "The first column (ID) is empty!"
      exit 1
   fi

   if [ "$col2" = "" ]; then
      echo "The second column (ref) is empty for ID $col1!"
      exit 2
   fi

   # If col3 (hyp) is empty, that may be that the ASR engine was not able to
   # produce a transcript.  In that case, put an "empty" string in col3.
   if [ "$col3" = "" ]; then
      col3="empty"
      flag_1="1"
      if [ "$flag_1_str" = "" ]; then
          flag_1_str="${col1}"
      else
         flag_1_str="${flag_1_str}, ${col1}"
      fi
   fi

   rm -fr foo && mkdir foo
   echo "$col2" > foo/ref
   echo "$col3" > foo/hyp
   $SCLITE_EXE -r foo/ref -h foo/hyp -i spu_id -s -o all 1>/dev/null 2>&1

   ref=`cat foo/hyp.pra | egrep "^REF" | cut -d " " --fields=3-`
   hyp=`cat foo/hyp.pra | egrep "^HYP" | cut -d " " --fields=3-`
   wer=`cat foo/hyp.sys | egrep "Sum/Avg" |\
	 cut -d'|' -f4 |\
	 tr -s ' ' |\
	 sed 's/^[ \t]*//' |\
	 sed 's/[ \t]*$//' |\
	 cut -d' ' -f5`
   echo "$col1|$ref|$hyp|$wer" >> $OUTPUT_FILE

   echo -n "."
done < $INPUT_FILE
/bin/rm -fr foo
echo 

if [ "$flag_1" = "1" ]; then
   echo "For some observations, the hyp column (third column) was "
   echo "blank.  This could happen if the ASR engine was not able "
   echo "to transcribe anything.  The IDs where this occurred were "
   echo "the following:"
   echo $flag_1_str
fi
