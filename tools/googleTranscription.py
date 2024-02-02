# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:16:47 2022

@author: jipoz
"""

import pandas as pd
from google.cloud import speech
import os
import io
import json


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r'C:\Users\jipoz\Desktop\IIT\TFM\key-file.json'


df = pd.DataFrame(columns=['ID', 'google_asr'])

# dirVoxceleb = '/mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v4'
dirVoxceleb = r'C:\Users\jipoz\Desktop\IIT\TFM\mixAudio_v4'



#############################################################################
#############################################################################


for i in range(200):
        
    for j in range(2):
    
        # audio = dirVoxceleb + '/separation/mix{}_separation_{}.wav'.format(i+1,j+1)
        audio_16k = dirVoxceleb + r'\separation\audios_16KHz\mix{}_separation_{}.wav'.format(i+1,j+1)
        # a = 'ffmpeg -i {} -ar 16000 {}'.format(audio,audio_16k)
        # os.system(a)

        client = speech.SpeechClient()
        file_name = os.path.join(os.path.dirname(__file__), audio_16k)
        
        with io.open(file_name, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz = 16000,
            audio_channel_count = 1,
            language_code = "en-US",
            enable_word_confidence = True,
            model = 'video',
        )
        
        response = client.recognize(request={"config": config, "audio": audio})     

        response_json = type(response).to_json(response)
                        
        with open(r'C:\Users\jipoz\Desktop\IIT\TFM\google_transcription_after_video\mix{}_separation_{}.json'.format(i+1,j+1), 'w') as json_file:
            json_data = json.dump(response_json, json_file)

        for result in response.results:
            print('Transcript {}: {}'.format(i+1,result.alternatives[0].transcript))            
            df1 = pd.DataFrame([['mix{}_separation_{}'.format(i+1,j+1),'{}'.format(result.alternatives[0].transcript)]],columns=['ID', 'google_asr'])
            df = pd.concat([df,df1], axis=0, ignore_index=True)


#############################################################################
#############################################################################

# export GOOGLE_APPLICATION_CREDENTIALS='/mnt/c/Users/jipoz/Desktop/IIT/TFM/key-file.json'            

print (df)
df.to_csv(r'C:\Users\jipoz\Desktop\IIT\TFM\google_transcription_after_video.csv', index = False, sep='|', encoding='utf-8')  

#############################################################################
#############################################################################

# audio1 = 'mix164_original_2'
# audio_16k = dirVoxceleb + '/audios_16KHz/' + audio1 + '.wav'

# client = speech.SpeechClient()
# file_name = os.path.join(os.path.dirname(__file__), audio_16k)

# with io.open(file_name, "rb") as audio_file:
#     content = audio_file.read()
#     audio = speech.RecognitionAudio(content=content)

# config = speech.RecognitionConfig(
#     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz = 16000,
#     audio_channel_count = 1,
#     language_code = "en-US",
#     enable_word_confidence = True,
#     model = 'video',
# )

# response = client.recognize(request={"config": config, "audio": audio})

# response_json = type(response).to_json(response)
                
# with open('/mnt/c/Users/jipoz/Desktop/IIT/TFM/google_transcription/' + audio1 + '.json' , 'w') as json_file:
#     json_data = json.dump(response_json, json_file)


# print(audio1)

# for result in response.results:
#     print('{}'.format(result.alternatives[0].transcript))
    
#############################################################################
#############################################################################