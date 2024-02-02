# wer-breakdown.r - Ingests the results-canonicalized.csv file that has the
# following files: ID, google_asr_before_sep, amazon_asr_before_sep,
# ground_truth, google_asr_after_sep, amazon_asr_after_sep.  Then, the program
# will create the following files:
#
# human-google-before.csv : contains ID, ground_truth, google_asr_before_sep
# human-amazon-before.csv : contains ID, ground_truth, amazon_asr_before_sep
# human-google-after.csv  : contains ID, ground_truth, google_asr_after_sep
# human-amazon-after.csv  : contains ID, ground_truth, amazon_asr_after_sep
# google-amazon-before.csv: contains ID, google_asr_before_sep, 
#                                                     amazon_asr_before_sep
# google-amazon-after.csv : contains ID, google_asr_after_sep, 
#                                                     amazon_asr_after_sep
#
# WER can then be performed using the align-wer.sh script on the above 6 files.

setwd("/tmp/speech-sep") # Or wherever ...

df <- read.csv("results-canonicalized.csv", header=T, sep='|')

tmp.df <- df[, c("ID", "ground_truth", "google_asr_before_sep")]
write.table(tmp.df, "human-google-before.csv", sep='|', row.names = F,
            quote = F)
rm(tmp.df)

tmp.df <- df[, c("ID",  "ground_truth", "amazon_asr_before_sep")]
write.table(tmp.df, "human-amazon-before.csv", sep='|', row.names = F,
            quote = F)
rm(tmp.df)

tmp.df <- df[, c("ID", "ground_truth", "google_asr_after_sep")]
write.table(tmp.df, "human-google-after.csv", sep='|', row.names = F,
            quote = F)
rm(tmp.df)

tmp.df <- df[, c("ID", "ground_truth", "amazon_asr_after_sep")]
write.table(tmp.df, "human-amazon-after.csv", sep='|', row.names = F,
            quote = F)
rm(tmp.df)

tmp.df <- df[, c("ID", "google_asr_before_sep", "amazon_asr_before_sep")]
write.table(tmp.df, "google-amazon-before.csv", sep='|', row.names = F,
            quote = F)
rm(tmp.df)

tmp.df <- df[, c("ID", "google_asr_after_sep", "amazon_asr_after_sep")]
write.table(tmp.df, "google-amazon-after.csv", sep='|', row.names = F,
            quote = F)
rm(tmp.df)




