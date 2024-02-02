This subdirectory contains the pairwise-columns from results-canonicalized.csv
upon which WER can be performed.

The WER results are as follows:

- Human / Google before separation WER: 19.15%
- Human / Amazon before separation WER: 12.95%

- Human / Google after  separation WER: 39.90%
- Human / Amazon after  separation WER: 33.05%

- Google / Amazon before separation WER: 25.02%
- Google / Amazon after  separation WER: 37.49% (see note below).

Note that the quality of the recordings for Google and Amazon ASRs for the 
after separation audio samples is not quite high enough to derive a WER for
all samples, therefore the problemmatic samples that do not have a reasonable
WER are excluded.  These are: 
- Rows 117, 168, 268 (NA)
- Rows 26, 49, 58, 73, 85, 219, 273, 304, 305, 317, 332, 347 (these samples 
 have enough S+I+D that WER > 100.0%).
