#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 08:44:19 2021

@author: mirandazachopoulou
"""

# %%Importing Libraries 

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

# %%Importing data file and cleaning 

#Importing Data  
data = pd.read_excel('/Users/mirandazachopoulou/Desktop/BA Report/Data_Final.xlsx')

# %%Composer overview 

composers_grouped = data.groupby(['Composer']).size().reset_index()

composers_grouped.columns = ['Composer', 'Count']

plt.figure(figsize=(18, 15))

sns.set(font_scale=2)

res = sns.barplot(x='Count',
            y='Composer', data=composers_grouped,
            order=composers_grouped.sort_values('Count',ascending = False).Composer)

plt.savefig('/Users/mirandazachopoulou/Desktop/BA Report/Plots/plot1.png', dpi=300)

# %%Variable Correlations 

df_plot = data[['danceability', 'energy', 'loudness', 'instrumentalness', 'valence', \
                'tempo', 'key', 'mode', 'chroma_stft', 'spectral_centroid', \
                'spectral_bandwidth', 'rolloff', 'zero_crossing_rate']]

plt.figure(figsize=(20, 13))
sns.set(font_scale=2)

sns.heatmap(df_plot.corr(), cmap="coolwarm", annot=True)

plt.savefig('/Users/mirandazachopoulou/Desktop/BA Report/Plots/plot2.png', dpi=300)


# %%Composition Features 

comp_features = ['chroma_stft', 'spectral_centroid', 'spectral_bandwidth','rolloff', 'zero_crossing_rate', 'mfcc1']

conditions = [ data["Symphony"] == 1, data["Concerto"] == 1, data["Quartet"] == 1, \
              data["Trio"] == 1, data["Sonata"] == 1]

choices = ["Symphony", "Concerto", "Quartet", "Trio", "Sonata"]

data["Comp_Label"] = np.select(conditions, choices, default="None")

sns.set(font_scale=1)

for i in comp_features: 
    plt.clf()
    sns.violinplot(x="Comp_Label", y=i, data=data[data.Comp_Label != 'None'])
    plt.savefig('/Users/mirandazachopoulou/Desktop/BA Report/Plots/plot3_' + i + '.png', dpi=300)




# %%Spectrograms

from matplotlib import pyplot as plt
from librosa import display
import librosa
import numpy as np

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

#file = '/Users/mirandazachopoulou/Desktop/BA Report/wav_red/Nocturne No 2 in E-Flat Major, Op 9 No 2_ID_1VNvsvEsUpuUCbHpVop1vo.wav'
#file = '/Users/mirandazachopoulou/Desktop/BA Report/wav_red/Symphony No 40 in G Minor, K 550 I Allegro molto_ID_1O2hifLpcfAItR4rbPZMZo.wav'
file = '/Users/mirandazachopoulou/Desktop/BA Report/wav_red/Elgar Cello Concerto in E Minor, Op 85 I Adagio - Moderato_ID_5cwPIak6Pg5HRuXpA5ecuO.wav'

sig, fs = librosa.load(file)
plt.axis('off')
S = librosa.feature.melspectrogram(y=sig, sr=fs)
librosa.display.specshow(librosa.power_to_db(S, ref=np.max))

plt.savefig('/Users/mirandazachopoulou/Desktop/BA Report/Plots/spectral_e.png', dpi=300)
    
    
# %%Extracting playlists 
  
import spotipy 
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.oauth2 import SpotifyClientCredentials 
import time 
import requests

#Setting up authorization manager (link to my Spotify Developer account) 
auth = SpotifyClientCredentials(client_id = 'client_id', #input client id here  
                                client_secret = 'client_secret') #input code here 

sp = spotipy.Spotify(auth_manager=auth)


#function to extract playlist track id's
#code from https://spotipy.readthedocs.io/en/2.19.0/
def getTrackIDs(user, playlist_id): 
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

#extracting tracks from the playlists made using the algorithm in algorithm.py
tracks_m = getTrackIDs('mirazach', '1jdpK8LW40SJlga9PhuxSB') #mozart
tracks_c = getTrackIDs('mirazach', '3Gih2AA013Xh6xXtMOKsUk') #chopin
tracks_e = getTrackIDs('mirazach', '4shsj0AOzvDIvmhQjm8PgN') #elgar

#converting to dataframes 
tracks_m = pd.DataFrame(tracks_m,columns=['TrackID']) 
tracks_c = pd.DataFrame(tracks_c,columns=['TrackID'])
tracks_e = pd.DataFrame(tracks_e,columns=['TrackID'])

#merging with the equivalent features of each track 
tracks_m = pd.merge(tracks_m, data, how='left', on='TrackID')
tracks_c = pd.merge(tracks_c, data, how='left', on='TrackID')
tracks_e = pd.merge(tracks_e, data, how='left', on='TrackID')

# %%Playlist Visualization

#Get avg statistics and compare to piece statistics 

tracks_m.name = 'Mozart'
tracks_c.name = 'Chopin'
tracks_e.name = 'Elgar'

tracks_m.col = '#cc8963'
tracks_c.col = '#5f9e6e'
tracks_e.col = '#5975a4'

#Key Distribution 

def keys(df): 
    #clearing other plots 
    plt.clf()
    #converting column to string 
    df['key'] = df['key'].astype(str)
    #setting font scale
    sns.set(font_scale=1)
    #producing histogram
    p=sns.countplot(data=df, x="key", color= df.col,
                    order=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
    #replacing the number with the equivalent note names
    p.set_xticklabels(['C','C#','D','D#','E','F','F#','G', 'G#', 'A', 'A#', 'B'])
    #axis labels + title
    p.set_ylabel("Number of Tracks")
    p.set_xlabel("Key")
    p.set_title(df.name + ' Playlist: Key Distribution')
    #saving
    plt.savefig('/Users/mirandazachopoulou/Desktop/BA Report/Plots/key_' + df.name + '.png', dpi=300)

keys(tracks_m)
keys(tracks_c)
keys(tracks_e)

#Mode Distribution 

def mode(df): 
    #clearing other plots 
    plt.clf()
    #setting font scale
    sns.set(font_scale=1)
    #producing histogram
    p=sns.countplot(data=df, x="mode", color= df.col)
    #replacing the number with the equivalent mode names
    p.set_xticklabels(['Minor','Major'])
    #axis labels + title
    p.set_ylabel("Number of Tracks")
    p.set_xlabel("Mode")
    p.set_title(df.name + ' Playlist: Mode Distribution')
    #saving
    plt.savefig('/Users/mirandazachopoulou/Desktop/BA Report/Plots/mode_' + df.name + '.png', dpi=300)

mode(tracks_m)
mode(tracks_c)
mode(tracks_e)


#also calculate sihlouette scores !!  


# %%Measuring Similarity Dataframe

#Calculating column averages 
playlists = pd.DataFrame(
    {'M_Playlist': tracks_m.mean(),
     'C_Playlist': tracks_c.mean(),
     'E_Playlist': tracks_e.mean()
    })


#Selecting 3 pieces from the dataset
pieces = data[data['TrackName'].isin(['Nocturne No. 2 in E-Flat Major, Op. 9 No. 2', \
                                 'Symphony No. 40 in G Minor, K. 550: I. Allegro molto', \
                                 'Elgar: Cello Concerto in E Minor, Op. 85: I. Adagio - Moderato'])]

#Dropping track name and trackid columns 
pieces = pieces.drop(['TrackName', 'TrackID'], axis=1)

#Transposing dataframe and setting composer names as column names 
pieces = pieces.set_index('Composer').T.rename_axis('Index')

#Renaming columns 
pieces.columns = ['M_Piece', 'C_Piece', 'E_Piece']

#Merging 
compare = pd.concat([pieces, playlists], axis=1)
    
#removing some rows 
compare=compare.drop(['acousticness', 'key', 'mode', 'duration_ms', 'Popularity', 'Born', 
                      'Symphony', 'Concerto', 'Quartet', 'Trio', 'Sonata'])

#Calculating % Differences 
compare['M_Delta'] = (compare['M_Playlist']-compare['M_Piece']) / compare['M_Piece']*100
compare['C_Delta'] = (compare['C_Playlist']-compare['C_Piece']) / compare['C_Piece']*100
compare['E_Delta'] = (compare['E_Playlist']-compare['E_Piece']) / compare['E_Piece']*100

#Plotting
compare.index.name = 'Variables'
compare.reset_index(inplace=True)

plt.figure(figsize=(7, 4))

plt.clf()
p = sns.barplot(x="Variables", y="M_Delta", data=compare[1:14], color=tracks_m.col, saturation=.5)
p.axhline(15, ls='--')
p.axhline(-15, ls='--')
p.set_title('Mozart Playlist Average vs Piece')
p.set_ylabel('% Difference')
p.set_xlabel('')
p.set_xticklabels(p.get_xticklabels(),rotation = 80)
plt.savefig('/Users/mirandazachopoulou/Desktop/BA Report/Plots/m_delta.png', dpi=300, bbox_inches='tight')

plt.clf()
p = sns.barplot(x="Variables", y="C_Delta", data=compare[1:14], color=tracks_c.col, saturation=.5)
p.axhline(15, ls='--')
p.axhline(-15, ls='--')
p.set_title('Chopin Playlist Average vs Piece')
p.set_ylabel('% Difference')
p.set_xlabel('')
p.set_xticklabels(p.get_xticklabels(),rotation = 80)
plt.savefig('/Users/mirandazachopoulou/Desktop/BA Report/Plots/c_delta.png', dpi=300, bbox_inches='tight')

plt.clf()
p = sns.barplot(x="Variables", y="E_Delta", data=compare[1:14], color=tracks_e.col, saturation=.5)
p.axhline(15, ls='--')
p.axhline(-15, ls='--')
p.set_title('Elgar Playlist Average vs Piece')
p.set_ylabel('% Difference')
p.set_xlabel('')
p.set_xticklabels(p.get_xticklabels(),rotation = 80)
plt.savefig('/Users/mirandazachopoulou/Desktop/BA Report/Plots/e_delta.png', dpi=300, bbox_inches='tight')


    
    

