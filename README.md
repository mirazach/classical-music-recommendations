# Classical Music Recommendations

MSc Business Analytics Final Project: Using Principal Components Analysis and K-Means clustering for classical music recommendations.

## Project Description 

The incorporation of machine learning techniques within the music industry has significantly transformed listeners’ experience by allowing for personalised recommendations. At the forefront of this evolution is Music Information Retrieval, a field that develops music analysis algorithms by extracting characteristics from audio files. The aim of this project was to exploit MIR by exploring an unsupervised learning approach that captures the attributes of western classical music and creates recommendations based on a selected piece. The model was built using different feature categories, and the dimensionality was reduced using PCA. K-Means clustering was then used to divide musical pieces into playlists. 

## File Descriptions

- **GSA.py:** The source code for the Generalised Spotify Analyser library
- **spotifyConstants.py:** A python script that includes Spotify Developer account credentials that are used within GSA’s functions
- **data_collection.py:** A python script that was used to collect music data from Spotify and extract relevant features
- **mp3_to_wav.R:** An R script used to convert mp3 to WAV files.
- **algorithm.py:** The main project algorithm that takes 3 select pieces as inputs, filters the dataset to include the relevant classical eras and performs PCA and K-Means clustering to produce similar playlist
- **EDA.py:** A python script that performs exploratory data analysis of the dataset and creates visualisations for the algorithm results

## Libraries Used 

- **Spotipy:** https://spotipy.readthedocs.io/en/2.19.0/
- **GSA:** https://github.com/OleAd/GeneralizedSpotifyAnalyser
- **Pydub:** https://github.com/jiaaro/pydub
- **LibROSA:** https://librosa.org
- **tuneR:** https://cran.r-project.org/web/packages/tuneR/tuneR.pdf


