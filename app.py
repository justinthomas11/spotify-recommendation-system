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
    data = pd.read_csv('data/processed/tracks_with_moods.csv')
    # Remap moods to be more relevant and accurate
    mood_map = {"Sad": "Melancholy", "Workout": "Calm", "Acoustic": "Workout", "Focus": "Upbeat"}
    if 'mood' in data.columns:
        data['mood'] = data['mood'].replace(mood_map)
    return data
    
df = load_data()
FEATURE_COLS = ['danceability', 'energy', 'valence', 'acousticness',
                'tempo', 'loudness', 'speechiness', 'instrumentalness']

#Sidebar
st.sidebar.title("🎵 Spotify RecSys")
mode = st.sidebar.radio("Choose Mode", ["Mood Playlist", "Song Similarity"])

#Main UI
def get_recommendations(track_name, data, feature_cols, n=10):
    matches = data[data['track_name'].astype(str).str.lower() == track_name.lower()]
    if matches.empty:
        return None
    song_idx = matches.index[0]
    song_vector = data.loc[song_idx, feature_cols].values.reshape(1, -1)
    all_vectors = data[feature_cols].values
    similarities = cosine_similarity(song_vector, all_vectors)[0]
    similar_indices = similarities.argsort()[::-1][1:n+1]
    
    results = data.iloc[similar_indices][['track_name', 'artists', 'track_genre', 'mood', 'popularity']]
    results['similarity_score'] = similarities[similar_indices].round(4)
    return results

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
    
    # Get unique songs and display with artist name
    valid_df = df.dropna(subset=['track_name', 'artists']).drop_duplicates(subset=['track_name']).sort_values('track_name')
    
    def format_song(idx):
        row = valid_df.loc[idx]
        return f"{row['track_name']} — {row['artists']}"

    selected_idx = st.selectbox("Search for a song", valid_df.index.tolist(), format_func=format_song, index=None, placeholder="Type to search for a song...")
    song_input = valid_df.loc[selected_idx, 'track_name'] if selected_idx is not None else None
    
    if st.button("Find Similar 🔄") and song_input:
        recs = get_recommendations(song_input, df, FEATURE_COLS)
        if recs is None:
            st.error(f"Song '{song_input}' not found in the dataset!")
        else:
            st.success(f"Top similar songs for '{song_input}':")
            for _, row in recs.iterrows():
                st.markdown(f"**{row['track_name']}** — {row['artists']}")
                st.caption(f"Mood: {row['mood']} | Genre: {row['track_genre']} | Similarity: {row['similarity_score']}")
        
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit")
