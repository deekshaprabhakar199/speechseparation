# speech-separation
In this project, our aim is to evaluate a pre-trained deep learning speech separation model.

200 pairs of utterances (400 utterances in total) randomly taken from the VoxCeleb dataset are evaluated as follows: Each pair of utterances is approximately the same duration (number of seconds), each pair of utterance is put through Amazon Transcribe and Google ASR engines to derive a transcript.  This transcript is compared to a human-generated ground truth to derive a WER of the pair of utterances before the mixing step.  Let's call this WER_a.

Next, each pair of utterances is mixed using sox(1).  The mix stream is presented to the pre-trained, deep learning speech separation model, which will separate the streams into their respective utterances.  The separated utterances are then put through Amazon Transcribe and Google ASR engines to derive a transcript.  The transcript corresponding to the separated utterances is then compared to the human-generated ground to derive a WER of the pair of utterances after the separation step.  Let's call this WER_b.

If the separation is perfect, WER_a == WER_b for each pair of utterances.

If there is noise, then WER_a ~ WER_b for each pair of utterances (i.e., they are approximately equal).  The error here is the difference between WER_a and WER_b.

The WER is one metric to evaluate the separation.  More metrics will be sought.
