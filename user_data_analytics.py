import datetime

import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import *
import song_recommendations


class Analytics:
    def __init__(self, data):
        self.data = data

        self.data.drop(
            ['username', 'platform', 'conn_country', 'ip_addr_decrypted', 'user_agent_decrypted', 'shuffle', 'skipped',
             'offline', 'offline_timestamp', 'incognito_mode', 'episode_name', 'episode_show_name',
             'spotify_episode_uri', 'reason_start', 'reason_end'], axis=1, inplace=True)
        na_ind = list(self.data[self.data['master_metadata_track_name'].isna()].index)
        self.data.drop(na_ind, inplace=True)
        self.data['ts'] = pd.to_datetime(self.data['ts'], infer_datetime_format=True)
        self.data.sort_values(by=['ts'], inplace=True)
        self.data.index = range(0, self.data.shape[0])
        # self.data['date'] = [d.date() for d in self.data['ts']]
        # self.data['time'] = [d.time() for d in self.data['ts']]
        # self.data['day_of_week'] = [d.day_name() for d in self.data['ts']]
        # self.data['year'] = [d.year for d in self.data['ts']]

        # self.yearly_data = list()
        # self.years = self.data['year'].unique()
        # for i in range(0, len(self.years)):
        #     temp = self.data[self.data['year'] == self.years[i]]
        #     self.yearly_data.append(temp)
        self.today = dt.datetime.now()
        self.dt_3mnths = self.today + relativedelta(months=-3)
        self.data_3mnths = self.data[data['ts'] >= self.dt_3mnths]
        self.tot_songs_3mnths = self.data_3mnths['spotify_track_uri'].unique()

        self.yearly_data = list()
        self.years = data['ts'].dt.year.unique()
        for i in range(0, len(self.years)):
            temp = data[data['ts'].dt.year == self.years[i]]
            self.yearly_data.append(temp)

        self.tot_artist_overall = self.data['master_metadata_album_artist_name'].unique()
        self.tot_songs_overall = self.data['spotify_track_uri'].unique()
        self.tot_albums_overall = self.data['master_metadata_album_album_name'].unique()
        self.dates_unique = self.data['ts'].dt.date.unique()
        self.unique_months = data['ts'].dt.strftime('%m/%y').unique()

        self.morn = [dt.time(6, 0, 0), dt.time(11, 59, 59)]
        self.afnoon = [dt.time(12, 0, 0), dt.time(17, 59, 59)]
        self.eve = [dt.time(18, 0, 0), dt.time(23, 59, 59)]
        self.night = [dt.time(0, 0, 0), dt.time(5, 59, 59)]
        self.time_of_day = [self.morn, self.afnoon, self.eve, self.night]
        self.td = ['Morning', 'Afternoon', 'Evening', 'Night']

    def listening_time(self):
        # tot_listening_time = 'Total listening time from ' + str(self.data['date'].min()) + ' to ' + \
        #                      str(self.data['date'].max()) + ' in minutes is ' + \
        #                      str(round(self.data['ms_played'].sum() / 60000, 2))

        listenting_time_yearly = list()
        for i in range(0, len(self.yearly_data)):
            listenting_time_yearly.append(self.yearly_data[i]['ms_played'].sum())
        df_listening_time_yearly = pd.DataFrame(list(zip(self.years, listenting_time_yearly)),
                                                columns=['Year', 'Total_listening_time_in_ms'])


        return df_listening_time_yearly

    def listening_time_monthly(self):
        listening_time_monthly = list()
        for i in range(0, len(self.unique_months)):
            temp = self.data[self.data['ts'].dt.strftime('%m/%y') == self.unique_months[i]]
            listening_time_monthly.append(temp['ms_played'].sum())
        df_listening_time_monthly = pd.DataFrame(list(zip(self.unique_months, listening_time_monthly)),
                                                 columns=['Month', 'Total_listening_time'])

        return df_listening_time_monthly

    def songs_listened(self):
        # tot_songs_listened = 'Total number of songs listened is ' + str(len(self.tot_songs_overall))

        songs_yearly = list()
        for i in range(0, len(self.yearly_data)):
            songs_yearly.append(self.yearly_data[i]['master_metadata_track_name'].unique().shape[0])
        df_songs_yearly = pd.DataFrame(list(zip(self.years, songs_yearly)), columns=['Year', 'Total_songs_listened'])

        return df_songs_yearly

    def songs_listened_new(self):
        new_songs_yearly = list()
        new_songs_yearly_count = list()
        for i in range(0, len(self.yearly_data)):
            temp = self.yearly_data[i]['master_metadata_track_name'].unique()
            new_songs_yearly_count.append(np.setdiff1d(temp, new_songs_yearly).shape[0])
            new_songs_yearly.extend(temp)
        df_new_songs_yearly = pd.DataFrame(list(zip(self.years, new_songs_yearly_count)),
                                           columns=['Year', 'New_songs_discovered'])

        return df_new_songs_yearly

    def songs_listened_monthly(self):
        songs_listened_monthly = list()
        for i in range(0, len(self.unique_months)):
            temp = self.data[self.data['ts'].dt.strftime('%m/%y') == self.unique_months[i]]
            songs_listened_monthly.append(len(temp['master_metadata_track_name'].unique()))
        df_songs_listened_monthly = pd.DataFrame(list(zip(self.unique_months, songs_listened_monthly)),
                                                 columns=['Month', 'Number_of_songs_listened'])

        return df_songs_listened_monthly

    def artists_listened(self):
        # tot_artists_listened = 'Total number of artists listened to is ' + str(len(self.tot_artist_overall))

        artists_yearly = list()
        for i in range(0, len(self.yearly_data)):
            artists_yearly.append(self.yearly_data[i]['master_metadata_album_artist_name'].unique().shape[0])
        df_artists_yearly = pd.DataFrame(list(zip(self.years, artists_yearly)),
                                         columns=['Year', 'Total_artists_listened_to'])

        return df_artists_yearly

    def artists_listened_new(self):
        new_artists_yearly = list()
        new_artists_yearly_count = list()
        for i in range(0, len(self.yearly_data)):
            temp = self.yearly_data[i]['master_metadata_album_artist_name'].unique()
            new_artists_yearly_count.append(np.setdiff1d(temp, new_artists_yearly).shape[0])
            new_artists_yearly.extend(temp)
        df_new_artist_yearly = pd.DataFrame(list(zip(self.years, new_artists_yearly_count)),
                                            columns=['Year', 'New_artists_discovered'])
        return df_new_artist_yearly

    def artists_listened_monthly(self):
        artists_listened_monthly = list()
        for i in range(0, len(self.unique_months)):
            temp = self.data[self.data['ts'].dt.strftime('%m/%y') == self.unique_months[i]]
            artists_listened_monthly.append(len(temp['master_metadata_album_artist_name'].unique()))
        df_artists_listened_monthly = pd.DataFrame(list(zip(self.unique_months, artists_listened_monthly)),
                                                   columns=['Month', 'Number_of_artists_listened'])
        return df_artists_listened_monthly

    def favorite_artist(self):
        artist_listentime_overall = list()
        artist_totsongs_overall = list()
        artist_songsplayed_overall = list()

        for i in range(0, len(self.tot_artist_overall)):
            temp = self.data[self.data['master_metadata_album_artist_name'] == self.tot_artist_overall[i]]
            artist_listentime_overall.append(temp['ms_played'].sum())
            artist_totsongs_overall.append(temp['master_metadata_track_name'].unique().shape[0])
            artist_songsplayed_overall.append(temp.shape[0])

        df = pd.DataFrame(list(
            zip(self.tot_artist_overall, artist_listentime_overall, artist_totsongs_overall,
                artist_songsplayed_overall)),
            columns=['Artist', 'Total_listening_time_in_ms', 'Total_no_of_songs_listened',
                     'No_of_times_played'])

        df['fav_artist_score'] = 1.5 * ((df['Total_listening_time_in_ms'] - df['Total_listening_time_in_ms'].min()) / (
                df['Total_listening_time_in_ms'].max() - df['Total_listening_time_in_ms'].min())) + \
                                 1.2 * ((df['Total_no_of_songs_listened'] - df['Total_no_of_songs_listened'].min()) /
                                        (df['Total_no_of_songs_listened'].max() - df[
                                            'Total_no_of_songs_listened'].min())) + \
                                 0.8 * ((df['No_of_times_played'] - df['No_of_times_played'].min()) /
                                        (df['No_of_times_played'].max() - df['No_of_times_played'].min()))

        df = df.sort_values(by=['fav_artist_score'], ascending=False).iloc[:50]
        df.index = range(0, 50)

        return df, df.iloc[:10]

    def favorite_artist_yearly(self):
        yearly_fav_artists = list()
        for i in range(0, len(self.years)):
            artist_listentime_overall = list()
            artist_totsongs_overall = list()
            artist_songsplayed_overall = list()
            # yearly_artists = self.data[self.data['year'] == self.years[i]]['master_metadata_album_artist_name'].unique()
            yearly_artists = self.data[self.data['ts'].dt.year == self.years[i]]['master_metadata_album_artist_name'].unique()
            for j in range(0, len(yearly_artists)):
                temp = self.yearly_data[i][
                    self.yearly_data[i]['master_metadata_album_artist_name'] == yearly_artists[j]]
                artist_listentime_overall.append(temp['ms_played'].sum())
                artist_totsongs_overall.append(temp['master_metadata_track_name'].unique().shape[0])
                artist_songsplayed_overall.append(temp.shape[0])

            df = pd.DataFrame(list(
                zip(yearly_artists, artist_listentime_overall, artist_totsongs_overall,
                    artist_songsplayed_overall)),
                columns=['Artist', 'Total_listening_time_in_ms', 'Total_no_of_songs_listened',
                         'No_of_times_played'])

            df['fav_artist_score'] = 1.5 * (
                    (df['Total_listening_time_in_ms'] - df['Total_listening_time_in_ms'].min()) / (
                    df['Total_listening_time_in_ms'].max() - df['Total_listening_time_in_ms'].min())) + \
                                     1.2 * ((df['Total_no_of_songs_listened'] - df[
                'Total_no_of_songs_listened'].min()) /
                                            (df['Total_no_of_songs_listened'].max() - df[
                                                'Total_no_of_songs_listened'].min())) + \
                                     0.8 * ((df['No_of_times_played'] - df['No_of_times_played'].min()) /
                                            (df['No_of_times_played'].max() - df['No_of_times_played'].min()))

            df = df.sort_values(by=['fav_artist_score'], ascending=False).iloc[:10]
            df.index = range(0, 10)
            yearly_fav_artists.append(df)

        return yearly_fav_artists, self.years

    def favorite_song(self):
        songs_name = list()
        songs_artist = list()
        songs_album = list()
        songs_listentime_overall = list()
        songs_timesplayed_overall = list()

        for i in range(0, len(self.tot_songs_overall)):
            temp = self.data[self.data['spotify_track_uri'] == self.tot_songs_overall[i]]
            songs_name.append(temp['master_metadata_track_name'].iloc[0])
            songs_artist.append(temp['master_metadata_album_artist_name'].iloc[0])
            songs_album.append(temp['master_metadata_album_album_name'].iloc[0])
            songs_listentime_overall.append(temp['ms_played'].sum())
            songs_timesplayed_overall.append(temp.shape[0])

        df = pd.DataFrame(list(zip(songs_name, songs_artist, songs_album, self.tot_songs_overall,
                                   songs_listentime_overall, songs_timesplayed_overall)), columns=['Song', 'Artist',
                                                                                                   'Album',
                                                                                                   'Spotify_track_uri',
                                                                                                   'Total_listening_time_in_ms',
                                                                                                   'No_of_times_played'])

        df['fav_song_score'] = 1.5 * ((df['Total_listening_time_in_ms'] - df['Total_listening_time_in_ms'].min()) / (
                df['Total_listening_time_in_ms'].max() - df['Total_listening_time_in_ms'].min())) + 1 * (
                                       (df['No_of_times_played'] - df['No_of_times_played'].min()) / (
                                       df['No_of_times_played'].max() - df['No_of_times_played'].min()))

        df = df.sort_values(by=['fav_song_score'], ascending=False).iloc[:50]
        df.index = range(0, 50)

        return df, df.iloc[:10]

    def favorite_song_yearly(self):
        yearly_fav_songs = list()
        for i in range(0, len(self.years)):
            songs_listentime_overall = list()
            songs_timesplayed_overall = list()
            songs_name = list()
            songs_artist = list()
            songs_album = list()
            # yearly_songs = self.data[self.data['year'] == self.years[i]]['master_metadata_track_name'].unique()
            yearly_songs = self.data[self.data['ts'].dt.year == self.years[i]]['spotify_track_uri'].unique()
            for j in range(0, len(yearly_songs)):
                temp = self.yearly_data[i][
                    self.yearly_data[i]['spotify_track_uri'] == yearly_songs[j]]
                songs_name.append(temp['master_metadata_track_name'].iloc[0])
                songs_artist.append(temp['master_metadata_album_artist_name'].iloc[0])
                songs_album.append(temp['master_metadata_album_album_name'].iloc[0])
                songs_listentime_overall.append(temp['ms_played'].sum())
                songs_timesplayed_overall.append(temp.shape[0])

            df = pd.DataFrame(list(zip(songs_name, songs_artist, songs_album, yearly_songs,
                    songs_listentime_overall, songs_timesplayed_overall)), columns=['Song', 'Artist', 'Album',
                    'Spotify_track_uri', 'Total_listening_time_in_ms', 'No_of_times_played'])

            df['fav_song_score'] = 1.5 * (
                        (df['Total_listening_time_in_ms'] - df['Total_listening_time_in_ms'].min()) / (
                        df['Total_listening_time_in_ms'].max() - df['Total_listening_time_in_ms'].min())) + 1 * (
                                           (df['No_of_times_played'] - df['No_of_times_played'].min()) / (
                                           df['No_of_times_played'].max() - df['No_of_times_played'].min()))

            df = df.sort_values(by=['fav_song_score'], ascending=False).iloc[:10]
            df.index = range(0, 10)
            yearly_fav_songs.append(df)

        return yearly_fav_songs, self.years

    def favorite_album(self):
        albums_listentime_overall = list()
        albums_timesplayed_overall = list()
        albums_artist = list()

        for i in range(0, len(self.tot_albums_overall)):
            temp = self.data[self.data['master_metadata_album_album_name'] == self.tot_albums_overall[i]]
            albums_artist.append(temp['master_metadata_album_artist_name'].iloc[0])
            albums_listentime_overall.append(temp['ms_played'].sum())
            albums_timesplayed_overall.append(temp.shape[0])

        df = pd.DataFrame(list(zip(self.tot_albums_overall, albums_artist, albums_listentime_overall,
                                   albums_timesplayed_overall)),
                          columns=['Album', 'Artist', 'Total_listening_time_in_ms', 'No_of_times_played'])

        df['fav_album_score'] = 1.5 * ((df['Total_listening_time_in_ms'] - df['Total_listening_time_in_ms'].min()) / (
                df['Total_listening_time_in_ms'].max() - df['Total_listening_time_in_ms'].min())) + 1 * (
                                        (df['No_of_times_played'] - df['No_of_times_played'].min()) / (
                                        df['No_of_times_played'].max() - df['No_of_times_played'].min()))

        df = df.sort_values(by=['fav_album_score'], ascending=False).iloc[:50]
        df.index = range(0, 50)

        return df, df.iloc[:10]

    def favorite_time(self):
        time_of_day_listentime = list()
        time_of_day_songsplayed = list()

        for i in range(0, 4):
            # temp = self.data[[d >= self.time_of_day[i][0] and d <= self.time_of_day[i][1] for d in self.data['time']]]
            temp = self.data[[d >= self.time_of_day[i][0] and d <= self.time_of_day[i][1]
                              for d in self.data['ts'].dt.time]]
            time_of_day_songsplayed.append(temp.shape[0])
            time_of_day_listentime.append(temp['ms_played'].sum())

        df = pd.DataFrame(list(zip(self.td, time_of_day_listentime, time_of_day_songsplayed)),
                          columns=['Time_of_day', 'Total_listening_time_in_ms', 'Total_songs_listened_to'])

        df['fav_timeofday_score'] = 1.5 * (
                    (df['Total_listening_time_in_ms'] - df['Total_listening_time_in_ms'].min()) / (
                    df['Total_listening_time_in_ms'].max() - df['Total_listening_time_in_ms'].min())) + 1 * (
                                            (df['Total_songs_listened_to'] - df['Total_songs_listened_to'].min()) / (
                                            df['Total_songs_listened_to'].max() - df['Total_songs_listened_to'].min()))

        df = df.sort_values(by=['fav_timeofday_score'], ascending=False).iloc[:50]
        df.index = range(0, 4)
        return df

    def favorite_day(self):
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        favday_listentime = list()
        favday_songsplayed = list()

        for i in weekdays:
            # temp = self.data[self.data['day_of_week'] == i]
            temp = self.data[self.data['ts'].dt.day_name() == i]
            favday_listentime.append(temp['ms_played'].sum())
            favday_songsplayed.append(temp.shape[0])

        df = pd.DataFrame(list(zip(weekdays, favday_listentime, favday_songsplayed)),
                          columns=['Day_of_the_week', 'Total_listening_time_in_ms', 'Total_songs_listened_to'])

        df['fav_day_score'] = 1.5 * ((df['Total_listening_time_in_ms'] - df['Total_listening_time_in_ms'].min()) / (
                df['Total_listening_time_in_ms'].max() - df['Total_listening_time_in_ms'].min())) + 1 * (
                                      (df['Total_songs_listened_to'] - df['Total_songs_listened_to'].min()) / (
                                      df['Total_songs_listened_to'].max() - df[
                                  'Total_songs_listened_to'].min()))

        df = df.sort_values(by=['fav_day_score'], ascending=False).iloc[:50]
        df.index = range(0, 7)

        return df

    def day_most_repeated_song(self):
        most_played_day = list()
        for i in range(0, len(self.dates_unique)):
            most_played_day.append(['nothing', 0, 'nothing', 'nothing', 'nothing'])

        for i in range(0, len(self.dates_unique)):
            # temp = self.data[self.data['date'] == self.dates_unique[i]]
            temp = self.data[self.data['ts'].dt.date == self.dates_unique[i]]
            temp_songs = temp['spotify_track_uri'].unique()
            for j in temp_songs:
                temp2 = temp[temp['spotify_track_uri'] == j]
                if temp2.shape[0] > most_played_day[i][1]:
                    most_played_day[i][0] = temp2['master_metadata_track_name'].iloc[0]
                    most_played_day[i][1] = temp2.shape[0]
                    most_played_day[i][2] = temp2['master_metadata_album_artist_name'].iloc[0]
                    most_played_day[i][3] = temp2['master_metadata_album_album_name'].iloc[0]
                    most_played_day[i][4] = j

        df = pd.DataFrame(most_played_day, columns=['Name_of_song', 'No_of_times_played', 'Artist', 'Album',
                                                    'Spotify_track_uri'])
        df.insert(loc=0, column='Date', value=self.dates_unique)
        df_most_played_singleday = df.sort_values(by=['No_of_times_played'], ascending=False).iloc[:50]
        df_most_played_singleday.index = range(0, 50)

        return df_most_played_singleday, df_most_played_singleday.iloc[:10]

    def day_highest_listening_time(self):
        day_listening_time = list()
        for i in range(0, len(self.dates_unique)):
            # temp = self.data[self.data['date'] == self.dates_unique[i]]
            temp = self.data[self.data['ts'].dt.date == self.dates_unique[i]]
            day_listening_time.append(temp['ms_played'].sum())

        df_day_listening_time = pd.DataFrame(list(zip(self.dates_unique, day_listening_time)),
                                             columns=['Date', 'Total_listening_time_in_ms'])
        df_day_listening_time = df_day_listening_time.sort_values(by=['Total_listening_time_in_ms'],
                                                                  ascending=False).iloc[:50]
        df_day_listening_time.index = range(0, 50)
        # df_day_listening_time['Date'] = df_day_listening_time['Date'].astype('object')
        df_day_listening_time['Date'] = [x.strftime('%d/%m/%Y') for x in df_day_listening_time['Date']]

        return df_day_listening_time, df_day_listening_time.iloc[:10]

    def day_most_songs_listened(self):
        day_songs_listened = list()
        for i in range(0, len(self.dates_unique)):
            # temp = self.data[self.data['date'] == self.dates_unique[i]]
            temp = self.data[self.data['ts'].dt.date == self.dates_unique[i]]
            day_songs_listened.append(len(temp['master_metadata_track_name'].unique()))

        df_day_songs_listened = pd.DataFrame(list(zip(self.dates_unique, day_songs_listened)),
                                             columns=['Date', 'Different_songs_listened'])
        df_day_songs_listened = df_day_songs_listened.sort_values(by=['Different_songs_listened'],
                                                                  ascending=False).iloc[:50]
        df_day_songs_listened.index = range(0, 50)
        df_day_songs_listened['Date'] = [x.strftime('%d/%m/%Y') for x in df_day_songs_listened['Date']]

        return df_day_songs_listened, df_day_songs_listened.iloc[:10]

    def fav_songs_3mnths(self):

        songs_name = list()
        songs_artist = list()
        songs_album = list()
        songs_listentime_overall = list()
        songs_timesplayed_overall = list()

        for i in range(0, len(self.tot_songs_3mnths)):
            temp = self.data_3mnths[self.data_3mnths['spotify_track_uri'] == self.tot_songs_3mnths[i]]
            songs_name.append(temp['master_metadata_track_name'].iloc[0])
            songs_artist.append(temp['master_metadata_album_artist_name'].iloc[0])
            songs_album.append(temp['master_metadata_album_album_name'].iloc[0])
            songs_listentime_overall.append(temp['ms_played'].sum())
            songs_timesplayed_overall.append(temp.shape[0])

        df = pd.DataFrame(list(zip(songs_name, songs_artist, songs_album, self.tot_songs_3mnths,
                                   songs_listentime_overall, songs_timesplayed_overall)), columns=['Song', 'Artist',
                                                                                                   'Album',
                                                                                                   'id',
                                                                                                   'Total_listening_time_in_mins',
                                                                                                   'No_of_times_played'])
        df['Total_listening_time_in_mins'] = df['Total_listening_time_in_mins'] / 60000

        df['fav_song_score'] = 0.5 * ((df['Total_listening_time_in_mins'] - df['Total_listening_time_in_mins'].min()) / (
                df['Total_listening_time_in_mins'].max() - df['Total_listening_time_in_mins'].min())) + 0.3 * (
                                       (df['No_of_times_played'] - df['No_of_times_played'].min()) / (
                                       df['No_of_times_played'].max() - df['No_of_times_played'].min()))

        df = df.sort_values(by=['fav_song_score'], ascending=False).iloc[:50]
        df.index = range(0, 50)
        df.drop(['Album', 'Total_listening_time_in_mins', 'No_of_times_played'], axis=1, inplace=True)
        ob = song_recommendations.Recommendations(df)
        recommendations = ob.generate_playlist_recos()
        print(recommendations.head())

        # df.to_csv('topsongs6months.csv')
        # df.to_csv('topsongs6months_100_features.csv')
        return df


