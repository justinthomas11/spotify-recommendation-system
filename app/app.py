{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "4a6cbe2d-d530-4cc2-9896-94c501af7e7f",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import pickle\n",
    "from sklearn.metrics.pairwise import cosine_similarity"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "efbba43d-abbd-43d7-9f65-bb85c3957a4c",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-04-04 11:41:14.881 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "#Page config\n",
    "st.set_page_config(\n",
    "    page_title=\"Spotify RecSys\",\n",
    "    page_icon=\"🎵\",\n",
    "    layout=\"wide\"\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "568b2599-c5dc-4b05-a2b7-7643506a3eeb",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-04-04 11:41:30.912 WARNING streamlit.runtime.caching.cache_data_api: No runtime found, using MemoryCacheStorageManager\n",
      "2026-04-04 11:41:30.914 WARNING streamlit.runtime.caching.cache_data_api: No runtime found, using MemoryCacheStorageManager\n",
      "2026-04-04 11:41:30.914 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:31.435 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\Admin\\anaconda3\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n",
      "2026-04-04 11:41:31.436 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:31.437 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:32.009 Thread 'Thread-3': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:32.025 Thread 'Thread-3': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:32.026 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:32.026 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "#Load data and models\n",
    "@st.cache_data   # caches so it doesn't reload on every interaction\n",
    "def load_data():\n",
    "    return pd.read_csv('../data/processed/tracks_with_moods.csv')\n",
    "df = load_data()\n",
    "FEATURE_COLS = ['danceability', 'energy', 'valence', 'acousticness',\n",
    "                'tempo', 'loudness', 'speechiness', 'instrumentalness']\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "369d0cc4-4bc4-458c-bb27-fdcddc21323e",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-04-04 11:41:52.173 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:52.174 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:52.174 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:52.175 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:52.176 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:52.176 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:52.177 Session state does not function when running a script without `streamlit run`\n",
      "2026-04-04 11:41:52.177 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:41:52.178 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "#Sidebar\n",
    "st.sidebar.title(\"🎵 Spotify RecSys\")\n",
    "mode = st.sidebar.radio(\"Choose Mode\", [\"Mood Playlist\", \"Song Similarity\"])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "509e097b-f83e-46f2-b748-79b4a6347508",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-04-04 11:42:07.377 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.378 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.386 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.387 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.388 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.388 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.389 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.389 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.390 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.390 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.391 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.391 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.392 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.392 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.393 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.393 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 11:42:07.394 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator(_root_container=1, _parent=DeltaGenerator())"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Main UI\n",
    "if mode == \"Mood Playlist\":\n",
    "    st.title(\"🎭 Mood-Based Playlist Generator\")\n",
    "    moods = df['mood'].dropna().unique().tolist()\n",
    "    selected_mood = st.selectbox(\"Select a Mood\", sorted(moods))\n",
    "    \n",
    "    if st.button(\"Generate Playlist 🎶\"):\n",
    "        playlist = df[df['mood'] == selected_mood]\\\n",
    "                    .sort_values('popularity', ascending=False)\\\n",
    "                    .head(10)\n",
    "        \n",
    "        for _, row in playlist.iterrows():\n",
    "            col1, col2 = st.columns([3, 1])\n",
    "            with col1:\n",
    "                st.markdown(f\"**{row['track_name']}** — {row['artists']}\")\n",
    "                st.caption(f\"Genre: {row['track_genre']} | Popularity: {row['popularity']}\")\n",
    "            # Audio preview (if track has a preview_url column)\n",
    "            # with col2:\n",
    "            #     if pd.notna(row.get('preview_url')):\n",
    "            #         st.audio(row['preview_url'])\n",
    "elif mode == \"Song Similarity\":\n",
    "    st.title(\"🔍 Find Similar Songs\")\n",
    "    song_input = st.text_input(\"Enter a song name\")\n",
    "    \n",
    "    if st.button(\"Find Similar 🔄\") and song_input:\n",
    "        # Call your get_recommendations() function here\n",
    "        pass\n",
    "st.sidebar.markdown(\"---\")\n",
    "st.sidebar.markdown(\"Built with ❤️ using Streamlit\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7a38147a-5317-4407-8f89-d37612ae6744",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
