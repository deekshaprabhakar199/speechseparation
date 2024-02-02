# Ideas
- General evaluation of separation effectiveness
  - How pitch correlates
  - How gender correlates
- To expand the dataset on which to do the above analysis, we can combine stream-1 with stream-3, stream-1 with stream-4, and so on.
- Associate meta data with each individual stream: gender, degree of background noise, etc.
- Run evaluation on additional models (so far we have not found any).

# Further work ideas
- Developing a RAILS speech separation model
- Expand the population from 200 mixtures to 500 mixtures.  The original work used 400 original streams to create 200 mixed streams.  The new work will use 600 original streams to create 300 mixed streams, for a total of 500 mixed streams.  The streams in the new work MUST NOT overlap with the streams from the original work.

# Maybe a separate project using the same model
- Characterize the effectiveness of the model to do noise reduction on a single stream (with background music, or background noise).  We will need to manually find samples for evaluation
