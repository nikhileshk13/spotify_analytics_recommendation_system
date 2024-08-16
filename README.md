# Analytics on Spotify User Data and Recommendation System
In this project I have done analytics on the Spotify Extended Streaming History data to find some listening statistics of the user and made a recommendation system that recommendations songs based on the recent listening patterns of the user. <br><br>
In the Spotify Extended Streaming History data each entry corresponds to a song/podcast being played along with the features as as listening time, artist name, album name, etc. Using this features it is possible to find various useful statistics from the data to understand the listening pattern of the user. 
<p>
  <img src="https://github.com/nikhileshk13/spotify_analytics_recommendation_system/blob/main/images/data_spotify.png">
</p>
The following image shows the different statistics I have found using this data: <br><br>
<p>
  <img src="https://github.com/nikhileshk13/spotify_analytics_recommendation_system/blob/main/images/stats.png">
</p>
The favorite songs, albums and artists are determined by a score calculated by assigning appropriate weights to each feature. 
<br><br>
<a href="https://nbviewer.org/github/nikhileshk13/spotify_analytics_recommendation_system/blob/main/spotify_userdata_analytics_plotly_final.ipynb">Click here to view the analytics</a>
<br><br>
For recommendations system a created a tfidf feature set and consine similarity to find the top 50 songs based on user's current listening habits.
<br>I used the following dataset <br>
<a href="https://www.kaggle.com/datasets/mrmorj/dataset-of-songs-in-spotify">Dataset link</a><br>
<br>This dataset has limitations since the number of songs in this dataset is limited so that list of recommended songs might not completelety refelct the currect listening habits of the user.
<br>Here's an example of recommended songs<br>
<p>
  <img src="https://github.com/nikhileshk13/spotify_analytics_recommendation_system/blob/main/images/recommendations.png">
</p>

