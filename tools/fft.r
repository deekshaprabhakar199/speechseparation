library(sound)
library(logging)

# FFT code from the following source:
# http://samcarcagno.altervista.org/psych/sound_proc/sound_proc_R.html

rm(list=ls())
setwd("/home/vkg/vail/2022/projects")
basicConfig()

file <- "/tmp/mozilla_vkg0/mix108.wav"

smpl <- loadSample(file)
if (duration(smpl) == 0) {
  logwarn("Length of %s is 0 bytes.", file)
  stop()
}

smpl_freq <- rate(smpl)
smpl_bits <- bits(smpl)
smpl_numeric <- sound(smpl) # Extract the waveform matrix.  These should be mono
# recordings, so there will only be one channel.  Shape of this matrix is 1xn, 
# where n = rate * duration.  If the recording is not mono, then grab one of
# the channels.
if (dim(smpl_numeric)[1] == 2) {
  smpl_numeric <- smpl_numeric[1, ]
  loginfo("Stereo channels detected, using only a mono channel.")
}

# Plot the sound wave in the time domain
time_array <- (0:(dim(smpl_numeric)[2]-1)) / smpl_freq
time_array <- time_array * 1000
str <- paste("Time domain for", file, "(Male)")
plot(time_array, smpl_numeric, type='l', col='black', xlab='Time (ms)', 
     ylab='Amplitude', main=str)
rm(str, time_array)

# Use FFT to plot in frequency domain
n <- length(smpl_numeric)
p <- fft(smpl_numeric)
nUniquePts <- ceiling((n+1)/2)
p <- p[1:nUniquePts] #select just the first half since the second half is a  
# mirror image of the first
p <- abs(p)  #take the absolute value, or the magnitude 

p <- p / n #scale by the number of points so that the magnitude does not 
# depend on the length of the signal or on its sampling frequency  
p <- p^2  # square it to get the power, if power is desired.

# multiply by two (see technical document for details)
# odd nfft excludes Nyquist point
if (n %% 2 > 0){
  p[2:length(p)] <- p[2:length(p)]*2 # we've got odd number of points fft
} else {
  p[2: (length(p) -1)] <- p[2: (length(p) -1)]*2 # we've got even number of 
  # points fft
}

freqArray <- (0:(nUniquePts-1)) * (smpl_freq / n) #  create the frequency array

str <- paste("Frequency domain for", file, "(Male)")
plot(freqArray/1000, 10*log10(p), type='l', col='black', 
     xlab='Frequency (kHz)', ylab='Power (dB)', main=str)
rm(str)
