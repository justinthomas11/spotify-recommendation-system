# Spotify Recommendation System

A machine learning-based web application that analyzes audio features to recommend Spotify tracks based on acoustic similarities and inferred musical moods. Built using Python, Scikit-Learn, and Streamlit.

## Features

*   **Song Similarity:** Employs a collaborative filtering-inspired approach using cosine similarity vectors to find tracks that share similar audio characteristics (e.g., danceability, energy, valence, acousticness, tempo, loudness) as any user-selected song.
*   **Mood-Based Playlist Generator:** Utilizes K-Means clustering to partition tracks into distinct, human-readable mood profiles (Melancholy, Party, Calm, Chill, Workout, Upbeat). It dynamically curates playlists tailored to the selected emotional landscape based on popularity metrics.

## Tech Stack

*   **Application Framework:** Streamlit
*   **Data Processing:** Pandas, NumPy
*   **Machine Learning:** Scikit-Learn (Cosine Similarity, K-Means Clustering)
*   **Audio Feature Analysis:** Spotify Web API (Track Attributes)

## Project Structure

*   `app.py`: The main Streamlit web application.
*   `notebooks/`: Jupyter notebooks detailing the Exploratory Data Analysis (EDA), feature engineering, K-Means clustering models, and recommender prototyping.
*   `data/processed/`: Contains the optimized and cleaned datasets with generated mood labels required by the application.
*   `requirements.txt`: Python package dependencies.

## Installation and Execution

1.  Clone this repository to your local environment.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Launch the Streamlit server:
    ```bash
    streamlit run app.py
    ```
