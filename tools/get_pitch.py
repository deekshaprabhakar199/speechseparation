import parselmouth
import glob
import numpy
import pandas as pd

files = glob.glob('../before-separation/wav/mix*.wav')
fname=[]
median_pitch=[]
mean_pitch=[]
max_pitch=[]
min_pitch=[]
median_intensity=[]
mean_intensity=[]
max_intensity=[]
min_intensity=[]

for file in files:
    snd=parselmouth.Sound(file)
    pitch=snd.to_pitch()
    pitch_values = pitch.selected_array['frequency']
    d = {'time': pitch.xs(), 'pitch': pitch_values}
    pitch_df = pd.DataFrame(d)
    pitch_file = file.replace('before-separation/wav/', 'eval-results/audio-qualities/pitch_').replace('.wav', '.csv')
    pitch_df.to_csv(pitch_file, index=False)

    intensity = snd.to_intensity()
    d = {'time': intensity.xs(), 'intensity': intensity.values[0]}
    intensity_df = pd.DataFrame(d)
    intensity_file = file.replace('before-separation/wav/', 'eval-results/audio-qualities/intensity_').replace('.wav', '.csv')
    intensity_df.to_csv(intensity_file, index=False)

    fname.append(file.split('/')[-1].split('.wav')[0])
    pitch_df=pitch_df[pitch_df['pitch']!=0]
    median_pitch.append(pitch_df['pitch'].median())
    mean_pitch.append(pitch_df['pitch'].mean())
    max_pitch.append(pitch_df['pitch'].max())
    min_pitch.append(pitch_df['pitch'].min())
    median_intensity.append(intensity_df['intensity'].median())
    mean_intensity.append(intensity_df['intensity'].mean())
    max_intensity.append(intensity_df['intensity'].max())
    min_intensity.append(intensity_df['intensity'].min())

d = {
    'ID': fname,
    'median_pitch': median_pitch,
    'mean_pitch': mean_pitch,
    'max_pitch': max_pitch,
    'min_pitch': min_pitch,
    'median_intensity': median_intensity,
    'mean_intensity': mean_intensity,
    'max_intensity': max_intensity,
    'min_intensity': min_intensity
}
df = pd.DataFrame(d)
master_file='../eval-results/recording_characteristics.csv'
master = pd.read_csv(master_file, sep='|')
master = master.merge(df, on='ID')
master.to_csv(master_file, sep='|', index=False)
