Download PRAAT (https://www.fon.hum.uva.nl/praat/)
To get the pitch, read in the wav file using the command:
  $ praat --open <media file>
  In the "Praat Objects" window, select "View and Edit"
  This will bring up a window with time-domain curve of the file and a spectrogram.  
  In the time-domain part of the window, select the portion of the media file for which pitch is desired (position the mouse at 0, for instance, and drag the mouse to the end; this will select all of the file).
  Click on Pitch->Pitch Listing
  That will bring up a window with the F0 values for the media file.  Save to a text file and convert to csv.
  
  See also https://medium.com/@neurodatalab/pitch-tracking-or-how-to-estimate-the-fundamental-frequency-in-speech-on-the-examples-of-praat-fe0ca50f61fd
