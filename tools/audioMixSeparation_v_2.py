# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:14:31 2022

@author: jipoz
"""

nMixtures = 200


def mixAudios():  

    import os
    import shutil
    from mutagen.wave import WAVE
    import operator
    import matplotlib.pyplot as plt
    import time
    import random
    import sys
    
    # dirVoxceleb = r'C:\Users\jipoz\Desktop\IIT\TFM\wav'
    dirVoxceleb = '/mnt/c/Users/jipoz/Desktop/IIT/TFM/wav'

    listAudio = []
    listAudioNormalize = []
    d = {}
    listLength = []
        
    integLoudTarget = -25       #  -70 to -5.0  ->  default -24.0
    loudRange = 7               #  1.0 to 20.0  ->  default 7.0 (NO EFFECT)
    maxTruePeak = -2            #  -9.0 to 0.0  ->  default -2.0 (NO EFFECT)   
    
    print('\nScript for creating {} audio mixes.\n'.format(nMixtures))

    #### CREATE SORTED LIST OF AUDIO LENGTHS ####
    
    t1 = time.time()
    for directory, dirs, files in os.walk(dirVoxceleb):
        for f in files:
            audioPath = '{}/{}'.format(directory,f)
            audio = WAVE(audioPath)
            audio_info = audio.info
            audioLength = int(audio_info.length)
            listLength.append(audioLength)
            if (audioLength >=4 and audioLength <= 10): 
                d[audioPath] = audioLength    
    
    t2 = time.time()
    totalTime = (t2-t1)/60
    print('\nDirectory analyzed in %.3f mins\n' % totalTime)
    sortedDict = sorted(d.items(), key=operator.itemgetter(1))
        
    #### PLOT AUDIO LENGTH DISTRIBUTION ####

    # plt.hist(listLength, bins = range(4,20), align='left')
    # plt.title('Audio Length Distribution')
    # plt.xlabel("Audio Length (s)")
    # plt.ylabel("Number of Utterances")
    # plt.xlim(4,20)
    # plt.show()
        
    #### CREATE AUDIO LIST FOR MIXTURE ####
    
    # print(sortedDict)
    
    for i in range(nMixtures):      
        length = random.randint(4,10)
        n = 0
        for i in sortedDict:
            if i[1] == length:
                n += 1
                listAudio.append(i)
                sortedDict.remove(i)
                audioNORM = i[0].replace('.wav','_NORM.wav')
                a = 'ffmpeg -i {} -af loudnorm=I={}:LRA={}:TP={} {}'.format(i[0],integLoudTarget,loudRange,maxTruePeak,audioNORM)
                os.system(a)
                listAudioNormalize.append(audioNORM)
                if n == 2:
                    break
    
    if len(listAudio) != nMixtures*2:
        print('List Audio Length Check Failure!')
        sys.exit()
        
    print('\nThe list with {} audios have been successfully created.\n'.format(len(listAudio)))
        
    #### CREATE THE MIXTURES ####
    
    freq = 8000
    
    for i in range(nMixtures):
        os.mkdir('/mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v2/mix{}_{}Hz'.format(i+1,freq))
        s = 'ffmpeg -y -i {} -i {} -ar {} -filter_complex "[0:0]volume=1.7[a];[1:0]volume=1.7[b];[a][b]amix=inputs=2:duration=longest" /mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v2/mix{}_{}Hz/mix{}_{}Hz.wav'.format(listAudioNormalize[0],listAudioNormalize[1],freq,i+1,freq,i+1,freq)
        os.system(s)
        shutil.copy(listAudioNormalize[0], '/mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v2/mix{}_{}Hz/originalAudio_1.wav'.format(i+1,freq))
        listAudioNormalize.pop(0)
        shutil.copy(listAudioNormalize[0], '/mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v2/mix{}_{}Hz/originalAudio_2.wav'.format(i+1,freq))
        listAudioNormalize.pop(0)
        
    print('\n{} audio mixtures have been successfully created.\n'.format(nMixtures))


def audioSeparation():
    
    print('\nLoading necessary modules...')

    import time
    from speechbrain.pretrained import SepformerSeparation
    import torchaudio
    
    t1 = time.time()
       
    pathAudios = '/mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v4'
    
    print('Creating SepformerSeparation Model...\n')
    
    model = SepformerSeparation.from_hparams(source='speechbrain/sepformer-whamr', 
                                             savedir='pretrained_models/sepformer-whamr')
           
    print('\nSeparating audio sources...\n')
    
    for i in range(nMixtures):
        tinit = time.time()
        est_sources = model.separate_file(path= pathAudios + '/mixes/mix{}.wav'.format(i+1)) 
        torchaudio.save(pathAudios + '/separation/mix{}_separation_1.wav'.format(i+1), est_sources[:, :, 0].detach().cpu(), 8000)
        torchaudio.save(pathAudios + '/separation/mix{}_separation_2.wav'.format(i+1), est_sources[:, :, 1].detach().cpu(), 8000)
        
        tfinal = time.time()
        texec = tfinal - tinit
        print('Separation {} completed in {:3f} s'.format(i+1, texec))
    
    t2 = time.time()
    totalTime = (t2-t1)/60
    
    print('\nSatisfactory Separation in %.3f m\n' % totalTime)
    

def organizeDirectory():
    
    import shutil
    
    directory2 = '/mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v2'
    directory3 = '/mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v3'

    for i in range(200):
        for j in range(2):
            shutil.copy(directory2 + '/mix{}_8000Hz/originalAudio_{}.wav'.format(i+1,j+1),directory3 + '/mix{}_original_{}.wav'.format(i+1,j+1))
            shutil.copy(directory2 + '/mix{}_8000Hz/separationAudio_{}.wav'.format(i+1,j+1),directory3 + '/mix{}_separation_{}.wav'.format(i+1,j+1))
          

def mixAudios2():  

    import os
    import shutil
    from mutagen.wave import WAVE
    import operator
    import matplotlib.pyplot as plt
    import time
    import random
    import sys
    import numpy
    
    # dirVoxceleb = r'C:\Users\jipoz\Desktop\IIT\TFM\wav'
    dirVoxceleb = '/mnt/c/Users/jipoz/Desktop/IIT/TFM/wav'

    listAudio = []
    listAudioNormalize = []
    d = {}
    listLength = []
        
    integLoudTarget = -25       #  -70 to -5.0  ->  default -24.0
    loudRange = 7               #  1.0 to 20.0  ->  default 7.0 (NO EFFECT)
    maxTruePeak = -2            #  -9.0 to 0.0  ->  default -2.0 (NO EFFECT)   
    
    print('\nScript for creating {} audio mixes.\n'.format(nMixtures))

    #### CREATE SORTED LIST OF AUDIO LENGTHS ####
    
    t1 = time.time()
    for directory, dirs, files in os.walk(dirVoxceleb):
        for f in files:
            audioPath = '{}/{}'.format(directory,f)
            audio = WAVE(audioPath)
            audio_info = audio.info
            audioLength = int(audio_info.length)
            listLength.append(audioLength)
            if (audioLength >=4 and audioLength <= 10): 
                d[audioPath] = audioLength    
    
    t2 = time.time()
    totalTime = (t2-t1)/60
    print('\nDirectory analyzed in %.3f mins\n' % totalTime)
    sortedDict = sorted(d.items(), key=operator.itemgetter(1))
        
    #### PLOT AUDIO LENGTH DISTRIBUTION ####

    # plt.hist(listLength, bins = range(4,20), align='left')
    # plt.title('Audio Length Distribution')
    # plt.xlabel("Audio Length (s)")
    # plt.ylabel("Number of Utterances")
    # plt.xlim(4,20)
    # plt.show()
        
    #### CREATE AUDIO LIST FOR MIXTURE ####
    
    # print(sortedDict)
    
    list4 = []
    list5 = []
    list6 = []
    list7 = []
    list8 = []
    list9 = []
    list10 = []
    
    for i in sortedDict:
        if i[1] == 4:
            list4.append(i[0])
        elif i[1] == 5:
            list5.append(i[0])
        elif i[1] == 6:
            list6.append(i[0])
        elif i[1] == 7:
            list7.append(i[0])
        elif i[1] == 8:
            list8.append(i[0])
        elif i[1] == 9:
            list9.append(i[0])
        elif i[1] == 10:
            list10.append(i[0])
               
    for i in range(nMixtures):
        length = random.randint(4,10)
        a1 = numpy.random.choice(locals()[f'list{length}'])
        listAudio.append(a1)
        locals()[f'list{length}'].remove(a1)
        audioNORM = a1.replace('.wav','_NORM.wav')
        c = 'ffmpeg -i {} -af loudnorm=I={}:LRA={}:TP={} {}'.format(a1,integLoudTarget,loudRange,maxTruePeak,audioNORM)
        os.system(c)
        listAudioNormalize.append(audioNORM)
        a2 = numpy.random.choice(locals()[f'list{length}'])
        listAudio.append(a2)
        locals()[f'list{length}'].remove(a2)
        audioNORM = a2.replace('.wav','_NORM.wav')
        c = 'ffmpeg -i {} -af loudnorm=I={}:LRA={}:TP={} {}'.format(a2,integLoudTarget,loudRange,maxTruePeak,audioNORM)
        os.system(c)
        listAudioNormalize.append(audioNORM)

    if len(listAudio) != nMixtures*2:
        print('List Audio Length Check Failure!')
        sys.exit()
     
    # print(listAudio)  
    # print(listAudioNormalize)
     
    print('\nThe list with {} audios have been successfully created.\n'.format(len(listAudio)))
        
    #### CREATE THE MIXTURES ####
    
    freq = 8000
    
    for i in range(200):
        if os.path.exists('/mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v4/mix{}_original_1.wav'.format(i+1)) == False:
            s = 'ffmpeg -y -i {} -i {} -ar {} -filter_complex "[0:0]volume=1.7[a];[1:0]volume=1.7[b];[a][b]amix=inputs=2:duration=longest" /mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v4/mixes/mix{}.wav'.format(listAudioNormalize[0],listAudioNormalize[1],freq,i+1)
            os.system(s)
            shutil.copy(listAudioNormalize[0], '/mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v4/mix{}_original_1.wav'.format(i+1))
            listAudioNormalize.pop(0)
            shutil.copy(listAudioNormalize[0], '/mnt/c/Users/jipoz/Desktop/IIT/TFM/mixAudio_v4/mix{}_original_2.wav'.format(i+1))
            listAudioNormalize.pop(0)
            
    print('\n{} audio mixtures have been successfully created.\n'.format(nMixtures))
  
  
########################################################
########################################################


# mixAudios2()
# audioSeparation()

########################################################
######################################################## 
 