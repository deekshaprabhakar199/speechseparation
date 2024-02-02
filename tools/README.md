# Various scripts for post-processing data

## Canonicalization
### Dependencies
Uses pandas and num2word:

`pip install pandas num2word`

### Usage
Use either `-i` or `-e` to specify which columns to process or exclude from processing.

`python3 canonicalize.py <input csv> <output csv> -i <space separated list of cols>`

## align-wer.sh
### Dependencies
sclite(1).  The sclite(1) binary is in the tools subdirectory.  It is compiled as an ELF 64-bit LSB executable, for x86-64 Linux systems.

### Usage
Run by invoking the name of the shell script.  See comment block for changing parameters such as the input file, output file, etc.

## wer-breakdown.r
Takes the results-canonicalized.csv file and produces 6 files from it from which the WER can be derived.

## fft.r
FFT code in R.  Audacity does FFTs as well: Analyze->Plot Spectrum, and then choose "Algorithm: Spectrum".  Doing FFT in R will be easier for programmability.
