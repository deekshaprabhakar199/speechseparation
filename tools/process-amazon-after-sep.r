# Quick (non-optimized) code to take the output from Amazon ASR after
# separation CSV file and merge it into results.csv.

library(stringr)

setwd("/home/vkg")
rm(list=ls())

df <- read.csv("results.csv", header=T, sep='|')
amazon.df <- read.csv("results-after-sep-amazon.csv", header=T, sep='|',
                      comment.char = '#')

for (i in 1:nrow(amazon.df)) {
  res     <- amazon.df[i, c("amazon_asr_after_sep")]
  idx_str <- amazon.df[i, c("ID")]
  idx_str <- str_replace(idx_str, "separation", "original")  # The index in
  # results.csv has the form "mix10_original_1", the index in the Amazon ASR
  # CSV file has the form "mix10_separation_1".  Substitute "original" for
  # "separation", find the row with that index in results.csv and update the
  # last column.
  index   <- which(df$ID == idx_str)
  df[index, c("amazon_asr_after_sep")] <- res
}
