import pandas as pd
import numpy as np
import re
import itertools
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Recommendations:
    def __init__(self, top_songs):
        self.top_songs = top_songs
        self.df_main = pd.read_csv(r'N:\spotify_content_based\data\data_updated.csv')
        self.complete_feature_set = pd.read_csv(r'N:\spotify_content_based\data\data_feature_set.csv')
        self.complete_feature_set.drop('Unnamed: 0', axis=1, inplace=True)
        self.df_main.drop('Unnamed: 0', axis=1, inplace=True)
        self.top_songs['id'] = [re.split('track:', self.top_songs['id'][i])[1] for i in range(0, self.top_songs.shape[0])]

        client_id = 'fe61ef751f4e4a969c6f5f8c9cd67e9f'
        client_secret = 'f6871924c66f489097044035ba8afdab'
        self.sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    def generate_playlist_feature(self, weight_factor):
        complete_feature_set_playlist = self.complete_feature_set[
            self.complete_feature_set['id'].isin(self.top_songs['id'].values)]
        complete_feature_set_playlist = complete_feature_set_playlist.merge(self.top_songs[['id', 'fav_song_score']],
                                                                            on='id', how='inner')
        complete_feature_set_nonplaylist = self.complete_feature_set[
            ~self.complete_feature_set['id'].isin(self.top_songs['id'].values)]

        playlist_feature_set = complete_feature_set_playlist.sort_values('fav_song_score', ascending=False)
        playlist_feature_set['weight'] = playlist_feature_set['fav_song_score'].apply(lambda x: weight_factor ** (-x))

        playlist_feature_set_weighted = playlist_feature_set.copy()
        playlist_feature_set_weighted.update(
            playlist_feature_set_weighted.iloc[:, :-4].mul(playlist_feature_set_weighted.weight, 0))
        playlist_feature_set_weighted_final = playlist_feature_set_weighted.iloc[:, :-4]
        playlist_feature_set_weighted_final['id'] = playlist_feature_set['id']

        return playlist_feature_set_weighted_final.sum(axis=0), complete_feature_set_nonplaylist

    def generate_playlist_recos(self):
        features, nonplaylist_features = self.generate_playlist_feature(1.1)
        nonplaylist_features.drop(list(
            set(nonplaylist_features.columns).difference(set(features.index))),
                                              axis=1, inplace=True)
        non_playlist_df = self.df_main[self.df_main['id'].isin(nonplaylist_features['id'].values)]
        non_playlist_df['sim'] = cosine_similarity(nonplaylist_features.drop('id', axis=1).values,
                                                   features.drop(labels='id').values.reshape(1, -1))[:, 0]
        non_playlist_df_top_40 = non_playlist_df.sort_values('sim', ascending=False).head(50)
        non_playlist_df_top_40['url'] = non_playlist_df_top_40['id'].apply(
            lambda x: self.sp.track(x)['album']['images'][1]['url'])
        non_playlist_df_top_40 = non_playlist_df_top_40.loc[:, ['id', 'name', 'artists', 'year', 'url']]
        non_playlist_df_top_40.reset_index(drop=True, inplace=True)

        return non_playlist_df_top_40

