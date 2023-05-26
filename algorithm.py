#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 17:48:53 2021

@author: mirandazachopoulou
"""

# %%Importing Libraries 

#Data Manipulation
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

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


# %%Importing data 

data = pd.read_excel('Data_Final.xlsx')


# %%Step 1: Selecting piece and extracting subset based on composer 

#Select random piece 
#piece = 'Nocturne No. 2 in E-Flat Major, Op. 9 No. 2' #Chopin
#piece = 'Symphony No. 40 in G Minor, K. 550: I. Allegro molto' #Mozart
piece = 'Elgar: Cello Concerto in E Minor, Op. 85: I. Adagio - Moderato' #Elgar


#Extract composer's birth year
yr = data.loc[data['TrackName']==piece, 'Born'].values[0]

#Filter based on composer's birth year (+-50 yrs)
data_filtered =  data[(data['Born'] >= yr-50) & (data['Born'] <= yr+50)]



# %%Step 2: Prepping and scaling dataset 

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

# Exporting as Dataframe 


# %%Step 3: Performing PCA 

pca = PCA() 

pca.fit(x)

ratios = pca.explained_variance_ratio_

np.set_printoptions(suppress=True)

print(ratios)

plt.figure(figsize=(10,8))
plt.plot(range(1,39), ratios.cumsum(), marker='o')

#Let's take the 10 principal components (>60% variance)

pca = PCA(n_components = 10)

pca.fit(x)

x_pca = pca.transform(x)

# %%Step 4: Obtaining optimal K 


# Elbow Method for K means
model = KMeans()

visualizer = KElbowVisualizer(model, k=(2,30), timings=False)
visualizer.fit(x_pca)        # Fit data to visualizer
visualizer.show()        # Finalize and render figure

# %%Step 5: Applying K Means 

k=10 # <---- Input optimal k 

kmeans = KMeans(n_clusters = k, init='k-means++')

kmeans.fit(x_pca)

clusters_df = pd.concat([data_filtered.reset_index(drop=True), pd.DataFrame(x_pca)], axis = 1 )

clusters_df['Labels'] = kmeans.labels_

silhouette_avg = silhouette_score(x_pca, kmeans.labels_)

print(silhouette_avg)

# %%Step 6: Filtering 

#Obtaining cluster label of chosen piece 

label = clusters_df.loc[clusters_df['TrackName']==piece, 'Labels'].values[0]

#Filtering to get pieces with same label 
data_label = clusters_df[clusters_df.Labels == label]

pieces = data_label.TrackID

# %%Step 7: Create Playlist 

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = 'client_id', #add client id
                                               client_secret = 'client_secret', #add client secret
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='playlist-modify-public'))

#converting pieces to a list instead of series 
pieces = list(pieces)

#shuffling pieces so that composers are not grouped together 
random.shuffle(pieces)

#playlist_id = '4shsj0AOzvDIvmhQjm8PgN' #Elgar
playlist_id = '1jdpK8LW40SJlga9PhuxSB' #Mozart
#playlist_id = '3Gih2AA013Xh6xXtMOKsUk' #Chopin

#Adding pieces in segments of 100 as Spotify does not allow you to add more at a time
sp.playlist_add_items(playlist_id, pieces[0:100],   position=None)
sp.playlist_add_items(playlist_id, pieces[100:200], position=None)


    
