#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 17:48:53 2021

@author: mirandazachopoulou
"""

# Importing Libraries 

#Data Manipulation
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

#Principal Components Analysis 
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

#K-means Clustering 
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.metrics import silhouette_score

#Spotify API 
import spotipy 
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.oauth2 import SpotifyClientCredentials 


#Recommendation Function 
def get_recommendation(data, piece, playlist_id, client_id, client_secret):

    ################################################################
    #STEP 1: Selecting piece and extracting subset based on composer 
    ################################################################

    #Extract composer's birth year
    yr = data.loc[data['TrackName']==piece, 'Born'].values[0]

    #Filter based on composer's birth year (+-50 yrs)
    data_filtered =  data[(data['Born'] >= yr-50) & (data['Born'] <= yr+50)]

    ####################################
    #STEP 2: Prepping and scaling dataset 
    ####################################

    #removing NA rows
    data_filtered = data_filtered.dropna()

    #Selecting relevant features 
    features = ['danceability', 'energy', 'loudness', \
                'instrumentalness', 'valence', 'tempo', 'key', 'mode', \
                'chroma_stft', 'spectral_centroid', 'spectral_bandwidth', 'rolloff', \
                'zero_crossing_rate', 'mfcc1', 'mfcc2', 'mfcc3', 'mfcc4', 'mfcc5', \
                'mfcc6', 'mfcc7', 'mfcc8', 'mfcc9', 'mfcc10', 'mfcc11', 'mfcc12', 'mfcc13', \
                'mfcc14', 'mfcc15', 'mfcc16', 'mfcc17', 'mfcc18', 'mfcc19', 'mfcc20', \
                'Symphony', 'Concerto', 'Quartet', 'Trio', 'Sonata']
        
    # Separating out the features
    x = data_filtered.loc[:, features].values

    # Standardizing the features
    x = StandardScaler().fit_transform(x)


    ########################
    # STEP 3: Performing PCA 
    ########################

    pca = PCA() 

    pca.fit(x)

    # ratios = pca.explained_variance_ratio_

    # np.set_printoptions(suppress=True)

    # plt.figure(figsize=(10,8))
    # plt.plot(range(1,39), ratios.cumsum(), marker='o')

    #Let's take the 10 principal components (>60% variance)
    pca = PCA(n_components = 10)

    pca.fit(x)

    x_pca = pca.transform(x)


    #############################
    # STEP 4: Obtaining optimal K 
    #############################

    # Elbow Method for K means
    model = KMeans(n_init=10)

    visualizer = KElbowVisualizer(model, k=(2,30), timings=False)
    visualizer.fit(x_pca)        
    visualizer.show()  

    while True:
        try:
            k = int(input("Enter optimal k: "))
        except ValueError:
            print("This is not a valid value for k.")
            continue
        else:
            break      

    ##########################
    # STEP 5: Applying K Means 
    ##########################

    kmeans = KMeans(n_clusters = k, init='k-means++', n_init=10)

    kmeans.fit(x_pca)

    clusters_df = pd.concat([data_filtered.reset_index(drop=True), pd.DataFrame(x_pca)], axis = 1 )

    clusters_df['Labels'] = kmeans.labels_

    #silhouette_avg = silhouette_score(x_pca, kmeans.labels_)

    #print(silhouette_avg)

    ###################
    # STEP 6: Filtering 
    ###################

    #Obtaining cluster label of chosen piece 
    label = clusters_df.loc[clusters_df['TrackName']==piece, 'Labels'].values[0]

    #Filtering to get pieces with same label 
    data_label = clusters_df[clusters_df.Labels == label]

    pieces = data_label.TrackID

    #########################
    # Step 7: Create Playlist 
    #########################

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id,
                                                client_secret = client_secret, 
                                                redirect_uri='http://localhost:8888/callback',
                                                scope='playlist-modify-public'))

    #converting pieces to a list instead of series 
    pieces = list(pieces)

    #shuffling pieces so that composers are not grouped together 
    random.shuffle(pieces)

    #Adding pieces in segments of 100 as Spotify does not allow you to add more at a time
    sp.playlist_add_items(playlist_id, pieces[0:100],   position=None)
    sp.playlist_add_items(playlist_id, pieces[100:200], position=None)

    print("Playlist Created")


#Helper Functions 

#function to extract playlist track id's
#code from https://spotipy.readthedocs.io/en/2.19.0/
def getTrackIDs(user, playlist_id, sp): 
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

#Function that visualises the key distribution of the playlists
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

    plt.show() 

#Function that visualises the mode distribution of the playlists
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

    plt.show()
