# Classical Music Recommendations

MSc Business Analytics Final Project: Using Principal Components Analysis and K-Means clustering for classical music recommendations.

## Project Description 

The incorporation of machine learning techniques within the music industry has significantly transformed listeners’ experience by allowing for personalised recommendations. At the forefront of this evolution is Music Information Retrieval, a field that develops music analysis algorithms by extracting characteristics from audio files. The aim of this project was to exploit MIR by exploring an unsupervised learning approach that captures the attributes of western classical music and creates recommendations based on a selected piece. The model was built using different feature categories, and the dimensionality was reduced using PCA. K-Means clustering was then used to divide musical pieces into playlists. 

## File Descriptions

**data**
- **Composers.xlsx:** An excel spreadsheet of 49 composers, including their spotify playlist URI and birth and death dates.
- **Data_Final.xlsx:** The final dataset that is used by the algorithm to make playlist recommendations.

**scripts** 
- **GSA.py:** The source code for the Generalised Spotify Analyser library
- **spotifyConstants.py:** A python script that includes Spotify Developer account credentials that are used within GSA’s functions
- **mp3_to_wav.R:** An R script used to convert mp3 to WAV files.
- **functions.ipynb:** A python script that contains helper functions for this project, including the playlist generation algorithm. 

**notebooks** 
- **01_data_collection.ipynb:** A jupyter notebook that can be used to collect music data from Spotify and extract relevant features
- **02_recommendations.ipynb:** A jupyter notebook that can be used to create playlists given a selected piece from the data_final.xlsx dataset. 


## Data

To create a training dataset, 49 classical composers' names were collected along with the links to their Spotify playlists and birth years. An algorithm was developed using Python's Spotipy and GSA libraries to extract track names and Spotify features from the playlists. Spectral features were obtained through the libROSA library by converting MP3 samples to WAV files using R's TuneR package. To manage computation, audio files were trimmed to 10 seconds using the pydub library. Additionally, Pandas was used to create a new feature category related to composition types, adding binary columns to indicate the presence of specific composition types in track titles. 

<img width="938" alt="data" src="https://github.com/mirazach/classical-music-recommendations/assets/78528123/90d63f30-170b-4147-850a-0e283fd8eac7">


## Usage

To create a new playlist you can follow the following steps: 
1. Clone this repository.
2. In your directory, create a `.env` file and specify your Spotify credentials as descibed in the [Spotipy documentation](https://spotipy.readthedocs.io/en/2.10.0/).
3. Open the `02_recommendations.ipynb` notebook. Specify the piece that you would like to to create a playlist for.
4. Create a new playlist on spotify and paste your playlist ID in the jupyter notebook.
5. Run the `get_recommendation()` function and, once prompted, input the optimal k value for the k-means clustering model.

Demo:
https://github.com/mirazach/classical-music-recommendations/assets/78528123/75a59508-1133-4983-a16c-be8bda0e1bde


## More information 

You can read the full report [here](https://github.com/mirazach/classical-music-recommendations/blob/4b8250664e65fea9d41e74f3b7a24cc8030c7044/Report.pdf)


## Libraries Used 

- **Spotipy:** https://spotipy.readthedocs.io/en/2.19.0/
- **GSA:** https://github.com/OleAd/GeneralizedSpotifyAnalyser
- **Pydub:** https://github.com/jiaaro/pydub
- **LibROSA:** https://librosa.org
- **tuneR:** https://cran.r-project.org/web/packages/tuneR/tuneR.pdf


