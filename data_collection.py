 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:18:00 2021

@author: mirandazachopoulou
"""

# %%Importing Libraries 

import pandas as pd
import numpy as np
import librosa
import os.path
import os 
import matplotlib.pyplot as plt
import spotipy 
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.oauth2 import SpotifyClientCredentials 
import time 
import requests
import GSA

# %% Establishing Spotify connection 

#Setting up authorization manager (link to my Spotify Developer account) 
auth = SpotifyClientCredentials(client_id = 'af3454dba3a342e3ad104421b402aaaa', 
                                client_secret = '13e88db67d294b9ea5d9e106c18d44f6')

sp = spotipy.Spotify(auth_manager=auth)

#Authenticate to access Spotify API through Spotipy
GSA.authenticate()

# %% Building initial dataset 

#Importing composers dataset 
composers = pd.read_excel('/Users/mirandazachopoulou/Desktop/BA Report/Composers.xlsx')

#Compiling information from all Playlists 

#Creating empty dataframe 
data = pd.DataFrame(columns = ['Composer', 'playlistID', 'TrackName', 'TrackID', 'SampleURL', 'ReleaseYear', 
                               'Genres', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 
                               'instrumentalness', 'liveness', 'valence', 'tempo', 'key', 'mode', 'duration_ms', 
                               'Popularity']) 

for i in range(0, len(composers)): 
    
    #Track progress 
    print(i)
    
    #Get composer 
    composer = composers.iloc[i,0]
    
    #Get playlist URI 
    uri = composers.iloc[i,2]
    
    #Obtain plylist information 
    playlist_info = GSA.getInformation(uri)
    
    #Turn into dataframe 
    playlist_info_df = pd.read_pickle(playlist_info)
   
    #Combine with composer name 
    composer_df = pd.DataFrame({'Composer': [composer]*len(playlist_info_df)})
    playlist_info_df = pd.concat([composer_df, playlist_info_df], axis=1)
    
    #Adding to overall dataframe 
    data = pd.concat([data, playlist_info_df]).reset_index(drop=True)
    

# %% Import dataframe 

#data.to_excel("/Users/mirandazachopoulou/Desktop/BA Report/Data.xlsx",  index=False) 
 
data = pd.read_excel('/Users/mirandazachopoulou/Desktop/BA Report/Data.xlsx')

len(data[data.SampleURL.isnull()])
#There's 188 missing samples so those rows will be removed  

data.dropna(subset = ["SampleURL"], inplace=True)
data = data.reset_index(drop=True)


# %% Obtaining mp3 samples (~30 minutes)

toDownload = data[['SampleURL', 'TrackName', 'TrackID', 'playlistID']].values.tolist()

# Create an array to keep track of which were successfully downloaded
downloaded = []

# Now download preview MP3s, in a loop

counter = 0 


for track in toDownload:
    
    success = GSA.downloadTracks(track)
    downloaded.append(success)
    
    #to keep track of progress
    counter += 1 
    if counter % 10 == 0:
        print(counter)
                                                            

# %% Trimming wav files 

from scipy.io import wavfile

file_names = os.listdir('/Users/mirandazachopoulou/Desktop/BA Report/wav')

# the timestamp to split at (in seconds)
timestamp_start = 5
timestamp_end = 15

for filename in file_names:
    
    if filename == '.DS_Store':
        continue 

    # read the file and get the sample rate and data
    rate, data = wavfile.read('/Users/mirandazachopoulou/Desktop/BA Report/wav/' + filename) 

    # get the frame to split at
    split_start = rate * timestamp_start
    split_end = rate * timestamp_end

    # split
    sample = data[split_start:split_end-1]  # split

    # save the result
    wavfile.write('/Users/mirandazachopoulou/Desktop/BA Report/wav_red/'+filename, rate, sample)
    
 # %% Extracting audio features 


#Dataframe column names 
colnames = ['filename', 'chroma_stft', 'spectral_centroid', 'spectral_bandwidth', 'rolloff', 'zero_crossing_rate']
for i in range(1, 21):
    colnames.append('mfcc'+str(i))

#Creating empty dataframe 
audio_features = pd.DataFrame(columns = colnames) 

#Getting filenames in the wav folder 
file_names = os.listdir('/Users/mirandazachopoulou/Desktop/BA Report/wav_red')

counter = 0 

#Looping through filenames
for filename in file_names:
    
    if filename == '.DS_Store':
        continue 
    
    #to keep track of progress
    counter += 1 
    if counter % 10 == 0:
        print(counter)
        
    y, sr = librosa.load('/Users/mirandazachopoulou/Desktop/BA Report/wav_red/' + filename)
    
    #Obtaining audio features 
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    values = [filename, np.mean(chroma_stft), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]   
    for e in mfcc:
        values.append(np.mean(e))

    
    #Adding row to dataframe 
    df_length = len(audio_features)
    audio_features.loc[len(audio_features)] = values
    
# %% Combining with data df

#audi features dataframe back up 
audio_features_bu = audio_features.copy()

#Extracting TrackIDs from filenames 
audio_features['TrackID'] = audio_features.filename.apply(lambda st: st[st.find("ID_")+3:st.find(".wav")])

#Merging 
data = pd.merge(data, audio_features, 'left', on='TrackID')


    
# %% Finalizing Dataframe 

data = pd.merge(data, composers[['Last Name', 'Born']], 'left', left_on='Composer', right_on='Last Name')

#Removing irrelevant columns 
data = data.drop(columns=['playlistID', 'SampleURL', 'ReleaseYear', \
                          'speechiness', 'liveness', 'Genres', 'filename', 'Last Name'])

#Removing Albinoni because only 4 pieces came through 
data = data[data['Composer']!='Albinoni']

# %%Creating some additional features 

data['Symphony'] = data["TrackName"].map(lambda x: 1 if "Symphony" in x else 0)
data['Concerto'] = data["TrackName"].map(lambda x: 1 if "Concerto" in x else 0)
data['Quartet'] = data["TrackName"].map(lambda x: 1 if "Quartet" in x else 0)
data['Trio'] = data["TrackName"].map(lambda x: 1 if "Trio" in x else 0)
data['Sonata'] = data["TrackName"].map(lambda x: 1 if "Sonata" in x else 0)

#Saving as an excel file 
data.to_excel("/Users/mirandazachopoulou/Desktop/BA Report/Data_Final.xlsx",  index=False) 













