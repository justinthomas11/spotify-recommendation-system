import pandas as pd

df = pd.read_csv('data/processed/tracks_with_moods.csv')
mood_labels = {
    0: 'Melancholy',
    1: 'Party',
    2: 'Calm',
    3: 'Chill',
    4: 'Workout',
    5: 'Upbeat'
}
df['mood'] = df['mood_cluster'].map(mood_labels)
df.to_csv('data/processed/tracks_with_moods.csv', index=False)
print("Moods updated successfully in tracks_with_moods.csv")
