from flask import Flask, render_template
import plotly.express as px
import plotly
import pandas as pd
import user_data_analytics
import json

loading=False
ld = list()
it = 0
while True:
    try:
        data = pd.read_json(r'my_spotify_data_jan24\MyData\endsong_' + str(it) + '.json')
        ld.append(data)
        it += 1
    except:
        break
data = ld[0]
for i in range(1, len(ld)):
    data = pd.concat([data, ld[i]])

ob = user_data_analytics.Analytics(data)

app = Flask(__name__, template_folder='tpt', static_folder='tpt')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/listening_time_yearly')
def listening_time_yearly():
    a = ob.listening_time()
    # fig = px.bar(b, x='Year', y="Total_listening_time_in_ms", title='Listening Time for Each Year',
    # labels={'Total_listening_time_in_ms': 'Listening Time in ms'})
    a['Total_listening_time_in_ms'] = (a['Total_listening_time_in_ms']/3600000).round(1)
    fig = px.pie(a, names='Year', values="Total_listening_time_in_ms", title='Listening Time for Each Year',
                 labels={'Total_listening_time_in_ms': 'Listening Time in hrs'}, hole=0.6)
    fig.update_traces(textposition='outside', textinfo='label+value+text')
    fig.update_layout(annotations=[dict(text='Total Listening Time',
                                        x=0.5, y=0.5, font_size=15, showarrow=False, align='center'),
                                   dict(text='(hrs)',
                                        x=0.5, y=0.42, font_size=15, showarrow=False, align='center'),
                                   dict(text=str(a['Total_listening_time_in_ms'].sum().round(1)),
                                        x=0.5, y=0.27, font_size=15, showarrow=False, align='center')])
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Listening Time for Each Year'
    description = 'This chart shows how the listening time has varied through each year'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/listening_time_monthly')
def listening_time_monthly():
    a = ob.listening_time_monthly()
    fig = px.line(a, x='Month', y="Total_listening_time",
                  title='Variation of Listening Time Each Month',
                  labels={'Total_listening_time': 'Listening Time in ms'})
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Monthly Variation of Listening Time'
    description = 'This chart shows how the listening time has varied each month'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/songs_listened_yearly')
def songs_listened_yearly():
    a = ob.songs_listened()
    fig = px.bar(a, x='Year', y="Total_songs_listened", title='Number of Songs Listened Each Year',
                 labels={'Total_songs_listened': 'Songs Listened'})
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Number of Songs Listened Each Year'
    description = 'This chart shows how the number of songs listened has varied through each year'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/songs_listened_monthly')
def songs_listened_monthly():
    a = ob.songs_listened_monthly()
    fig = px.line(a, x='Month', y="Number_of_songs_listened",
                  title='Variation of Songs Listened Each Month',
                  labels={'Number_of_songs_listened': 'Number of Songs Listened'})
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Monthly Variation of Number of Songs Listened'
    description = 'This chart shows how the number of songs listened has varied each month'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/artists_listened_yearly')
def artists_listened_yearly():
    a = ob.artists_listened()
    fig = px.bar(a, x='Year', y="Total_artists_listened_to", title='Number of Artists Listened Each Year',
                 labels={'Total_artists_listened_to': 'Artists Listened'})
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Number of Artists Listened Each Year'
    description = 'This chart shows how the number of artists listened to has varied through each year'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/artists_listened_monthly')
def artists_listened_monthly():
    a = ob.artists_listened_monthly()
    fig = px.line(a, x='Month', y="Number_of_artists_listened",
                  title='Variation of Artists Listened to Each Month',
                  labels={'Number_of_artists_listened': 'Number of Artists Listened to'})
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Monthly Variation of Number of Artists Listened to'
    description = 'This chart shows how the number of artists listened to has varied each month'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/new_songs_discovered')
def new_songs_discovered():
    a = ob.songs_listened_new()
    fig = px.pie(a, names='Year', values="New_songs_discovered", title='New Songs Discovered Each Year',
                 labels={'New_songs_discovered': 'New Songs Discovered'}, hole=0.6)
    fig.update_traces(textposition='outside', textinfo='label+value+text')
    fig.update_layout(annotations=[dict(text='Total Songs Listened',
                                        x=0.5, y=0.5, font_size=15, showarrow=False, align='center'),
                                   dict(text=str(a['New_songs_discovered'].sum()),
                                        x=0.5, y=0.4, font_size=15, showarrow=False, align='center')])
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'New Songs Discovered Each Year'
    description = 'This chart shows the number of new songs that were discovered each year as well as the total ' \
                  'number of songs listened to till now'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/new_artists_discovered')
def new_artists_discovered():
    a = ob.artists_listened_new()
    fig = px.pie(a, names='Year', values="New_artists_discovered", title='New Artists Discovered Each Year',
                 labels={'New_artists_discovered': 'New Artists Discovered'}, hole=0.6)
    fig.update_traces(textposition='outside', textinfo='label+value+text')
    fig.update_layout(annotations=[dict(text='Total Artists Listened',
                                        x=0.5, y=0.5, font_size=15, showarrow=False, align='center'),
                                   dict(text=str(a['New_artists_discovered'].sum()),
                                        x=0.5, y=0.4, font_size=15, showarrow=False, align='center')])
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'New Artists Discovered Each Year'
    description = 'This chart shows the number of new artists that were discovered each year as well as the total ' \
                  'number of artists listened to till now'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/fav_artists_overall')
def fav_artists_overall():
    a, b = ob.favorite_artist()
    b['Total_listening_time_in_ms'] = (b['Total_listening_time_in_ms'] / 60000).round(1)
    fig = px.bar(b, x='Artist', y="fav_artist_score", color='Artist', title='Top 10 Favorite Artists Overall',
                 labels={'fav_artist_score': 'Score', 'Total_listening_time_in_ms': 'Listening Time in ms',
                         'Total_no_of_songs_listened': 'Number of Songs Listened',
                         'No_of_times_played': 'Number of Times Played'},
                 hover_data=['Total_listening_time_in_ms', 'Total_no_of_songs_listened', 'No_of_times_played'])
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Favorite Artists Overall'
    description = 'This chart shows the favorite artists overall. The favorite artists are determined by a score' \
                  ' calculated using metrics such as the total listening time of an artist, number of times played and ' \
                  ' the total number of songs listened to.'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/fav_artist_yearly')
def fav_artist_yearly():
    a, b = ob.favorite_artist_yearly()
    figs = list()
    for i in range(0, len(a)):
        fig = px.bar(a[i], x='Artist', y="fav_artist_score", color='Artist',
                     title='Top 10 Favorite Artists for the Year ' + str(b[i]),
                     labels={'fav_artist_score': 'Score', 'Total_listening_time_in_ms': 'Listening Time in ms',
                             'Total_no_of_songs_listened': 'Number of Songs Listened',
                             'No_of_times_played': 'Number of Times Played'},
                     hover_data=['Total_listening_time_in_ms', 'Total_no_of_songs_listened', 'No_of_times_played'])
        figs.append(fig)
    header = 'Favorite Artists for Each Year'
    description = 'These charts shows the favorite artists for each year. The favorite artists are determined by a ' \
                  'score calculated using metrics such as the total listening time of an artist, number of times ' \
                  'played and the total number of songs listened to.'
    return render_template('test_flask_yearly.html', graph=figs, header=header, description=description)


@app.route('/fav_songs_overall')
def fav_songs_overall():
    a, b = ob.favorite_song()
    c = ob.fav_songs_3mnths()
    b['Total_listening_time_in_ms'] = (b['Total_listening_time_in_ms'] / 60000).round(1)
    fig = px.bar(b, x='Song', y="fav_song_score", color='Song', title='Top 10 Favorite Songs Overall',
                 labels={'fav_song_score': 'Score', 'Total_listening_time_in_ms': 'Listening Time in ms',
                         'No_of_times_played': 'Number of Times Played', 'Spotify_track_uri': 'Spotify Track URI'},
                 hover_data=['Artist', 'Album', 'Total_listening_time_in_ms', 'No_of_times_played', 'Spotify_track_uri'])
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Favorite Songs Overall'
    description = 'This chart shows the favorite songs overall. The favorite songs are determined by a score' \
                  ' calculated using metrics such as the total listening time of a song and the number of times that ' \
                  'song has been played.'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/fav_songs_yearly')
def fav_songs_yearly():
    a, b = ob.favorite_song_yearly()
    figs = list()
    for i in range(0, len(a)):
        fig = px.bar(a[i], x='Song', y="fav_song_score", color='Song',
                     title='Top 10 Favorite Artists for the Year ' + str(b[i]),
                     labels={'fav_song_score': 'Score', 'Total_listening_time_in_ms': 'Listening Time in ms',
                             'No_of_times_played': 'Number of Times Played', 'Spotify_track_uri': 'Spotify Track URI'},
                     hover_data=['Artist', 'Album', 'Total_listening_time_in_ms', 'No_of_times_played',
                                 'Spotify_track_uri'])
        figs.append(fig)
    header = 'Favorite Songs for Each Year'
    description = 'These charts shows the favorite songs for each year. The favorite songs are determined by a ' \
                  'score calculated using metrics such as the total listening time of a song and number of times that ' \
                  'song has been played.'
    return render_template('test_flask_yearly.html', graph=figs, header=header, description=description)


@app.route('/fav_albums')
def fav_albums():
    a, b = ob.favorite_album()
    b['Total_listening_time_in_ms'] = (b['Total_listening_time_in_ms'] / 60000).round(1)
    fig = px.bar(b, x='Album', y="fav_album_score", color='Album', title='Top 10 Favorite Albums',
                 labels={'fav_album_score': 'Score', 'Total_listening_time_in_ms': 'Listening Time in ms',
                         'No_of_times_played': 'Number of Times Played'},
                 hover_data=['Artist', 'Total_listening_time_in_ms', 'No_of_times_played'])
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Favorite Albums Overall'
    description = 'This chart shows the favorite albums overall. The favorite albums are determined by a score' \
                  ' calculated using metrics such as the total listening time of an album and the number of times ' \
                  'any song from the album has been played.'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/fav_time')
def fav_time():
    a = ob.favorite_time()
    fig = px.bar(a, x='Time_of_day', y="fav_timeofday_score", color='Time_of_day',
                 title='Favorite Time of the Day for Listening',
                 labels={'fav_timeofday_score': 'Score', 'Total_listening_time_in_ms': 'Listening Time in ms',
                         'Total_songs_listened_to': 'Total Songs Listened to', 'Time_of_day': 'Time of the Day'},
                 hover_data=['Total_listening_time_in_ms', 'Total_songs_listened_to'])
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Favorite Time of the Day for Listening'
    description = 'This chart shows the favorite time of the day (ie morning, afternoon, evening and night) for ' \
                  'listening. The favorite time is determined by a score calculated using metrics such as the total ' \
                  'listening time for that time of the day, number of songs that have been played during that time ' \
                  'of that day.'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/fav_day')
def fav_day():
    a = ob.favorite_day()
    fig = px.bar(a, x='Day_of_the_week', y="fav_day_score", color='Day_of_the_week',
                 title='Favorite Day of the Week for Listening',
                 labels={'fav_day_score': 'Score', 'Total_listening_time_in_ms': 'Listening Time in ms',
                         'Total_songs_listened_to': 'Total Songs Listened to', 'Day_of_the_week': 'Day of the Week'},
                 hover_data=['Total_listening_time_in_ms', 'Total_songs_listened_to'])
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Favorite Day of Week for Listening'
    description = 'This chart shows the favorite day of the week for listening. The favorite day is determined by a ' \
                  'score calculated using metrics such as the total listening time for that day, number of songs ' \
                  'that have been played that day '
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/most_repeated_song')
def most_repeated_song():
    a, b = ob.day_most_repeated_song()
    fig = px.bar(b, x='Name_of_song', y="No_of_times_played", color='Name_of_song',
                 title='Songs that were most repeated in a single day',
                 labels={'No_of_times_played': 'Number of Times Played', 'Name_of_song': 'Name of the Song',
                         'Spotify_track_uri':'Spotify Track URI'},
                 hover_data=['Date', 'Artist', 'Album', 'Spotify_track_uri'])
    fig.update_xaxes(showticklabels=False)
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Songs that were Most Repeated in a Single Day'
    description = 'This chart shows the songs that were most repeated in a single day'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/day_highest_time')
def day_highest_time():
    a, b = ob.day_highest_listening_time()
    b['Total_listening_time_in_ms'] = (b['Total_listening_time_in_ms'] / 3600000).round(1)
    fig = px.bar(b, x='Date', y="Total_listening_time_in_ms", color='Date',
                 title='Days with the Highest Listening Time',
                 labels={'Total_listening_time_in_ms': 'Listening Time in hrs'})
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Days which had the Highest Listening Time'
    description = 'This chart shows the days which had the highest listening time'
    return render_template('test_flask.html', graph=graph, header=header, description=description)


@app.route('/day_most_songs')
def day_most_songs():
    a, b = ob.day_most_songs_listened()
    fig = px.bar(b, x='Date', y="Different_songs_listened", color='Date',
                 title='Days which had the most songs listened ',
                 labels={'Different_songs_listened': 'Number of Songs Listened'})
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = 'Days with most Songs Listened to'
    description = 'This chart shows the days which had the most number of songs listened to'
    return render_template('test_flask.html', graph=graph, header=header, description=description)

# @app.route('/recommendations')
# def recommendations():

app.run(debug=True)
