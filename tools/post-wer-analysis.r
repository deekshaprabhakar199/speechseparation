rm(list=ls())
setwd("/home/vkg/speech-separation/")
google.before.df <- read.csv("eval-results/human-google-before-Aligned.csv", 
                             header=T, sep='|')
google.after.df <- read.csv("eval-results/human-google-after-Aligned.csv", 
                            header=T, sep='|')
google.indx <- which(google.after.df$wer < google.before.df$wer)
#----
amazon.before.df <- read.csv("eval-results/human-amazon-before-Aligned.csv", 
                             header=T, sep='|')
amazon.after.df <- read.csv("eval-results/human-amazon-after-Aligned.csv", 
                            header=T, sep='|')
amazon.indx <- which(amazon.after.df$wer < amazon.before.df$wer)
#-----
mix.df <- read.csv("eval-results/MOSnet_analysis/MOSnet_results_before_after.csv", 
                   header=T)
mix.indx <- which(mix.df$separation > mix.df$original)


