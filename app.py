import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

#Page config
st.set_page_config(
    page_title="Spotify RecSys",
    page_icon="🎵",
    layout="wide"
)

#Load data and models
@st.cache_data   # caches so it doesn't reload on every interaction
def load_data():
    return pd.read_csv('data/processed/tracks_with_moods.csv')
    
df = load_data()
FEATURE_COLS = ['danceability', 'energy', 'valence', 'acousticness',
                'tempo', 'loudness', 'speechiness', 'instrumentalness']

#Sidebar
st.sidebar.title("🎵 Spotify RecSys")
mode = st.sidebar.radio("Choose Mode", ["Mood Playlist", "Song Similarity"])

#Main UI
if mode == "Mood Playlist":
    st.title("🎭 Mood-Based Playlist Generator")
    moods = df['mood'].dropna().unique().tolist()
    selected_mood = st.selectbox("Select a Mood", sorted(moods))
    
    if st.button("Generate Playlist 🎶"):
        playlist = df[df['mood'] == selected_mood]\
                    .sort_values('popularity', ascending=False)\
                    .head(10)
        
        for _, row in playlist.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{row['track_name']}** — {row['artists']}")
                st.caption(f"Genre: {row['track_genre']} | Popularity: {row['popularity']}")
            # Audio preview (if track has a preview_url column)
            # with col2:
            #     if pd.notna(row.get('preview_url')):
            #         st.audio(row['preview_url'])
elif mode == "Song Similarity":
    st.title("🔍 Find Similar Songs")
    song_input = st.text_input("Enter a song name")
    
    if st.button("Find Similar 🔄") and song_input:
        # Call your get_recommendations() function here
        pass
        
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit")
