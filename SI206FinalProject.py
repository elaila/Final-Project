# Title: SI 206 Final Project
# Name : Laila Elnaggar

# Import Statements
import sqlite3 as sqlite
import spotipy
import spotipy.util as util
import matplotlib.pyplot as plt

def SetUp():
    client_id = '1a6bfcbf8b464425b9c13979147039f2'
    client_secret = 'd027afdff2c6477bb4620301d30faf0f'
    redirect_uri = 'http://localhost:8888/callback'

    username = 'laila.elnaggar'
    scope = 'user-library-read'

    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

    if token:
        sp = spotipy.Spotify(auth = token)
    return sp

artist_dict = {'Travis Scott': '0Y5tJX1MQlPlqiwlOH1tJY',
                'Drake': '3TVXtAsR1Inumwj472S9r4',
                'Billie Eilish': '6qqNVTkY8uBg9cP3Jd7DAH',
                'Kanye West': '5K4W6rqBFWDnAN6FQUkS6x',
                'Khalid': '6LuN9FCkKOj5PcnpouEgny',
                'Halsey': '26VFTg2z8YR0cCuwLzESi2',
                'Ariana Grande': '66CXWjxzNUsdJxJ2JdwvnR',
                'SZA': '7tYKF4w9nC0nq9CsPZTHyP',
                'Maroon 5': '04gDigrS5kc9YWfZHwBETP',
                'Shawn Mendes': '7n2wHs1TKAczGzO7Dd2rGr'}

def getTopTracks(API, artist_dict):
    track_info_list = []

    for artist in artist_dict.items():
        link = 'spotify:artist:' + artist[1]
        results = API.artist_top_tracks(link)

        for track in results['tracks'][:10]:
            track_name = track['name']
            release_date = track['album']['release_date']
            album_name = track['album']['name']
            artist_name = artist[0]
            popularity = track['popularity']
            track_info_list.append((track_name, release_date, album_name, artist_name, popularity))

    return track_info_list

def setUpSpotifyTable(track_info_list):
    conn = sqlite.connect('Spotify.sqlite')
    cur = conn.cursor()

    cur.execute(''' DROP TABLE IF EXISTS spotify ''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS spotify (track_name TEXT,
                                                        release_date DATETIME,
                                                        album_name TEXT,
                                                        artist_name TEXT,
                                                        popularity INTEGER)''')
    for info in track_info_list:
        cur.execute(''' INSERT INTO Spotify (track_name, release_date, album_name, artist_name, popularity)
                    VALUES (?, ?, ?, ?, ?)''',
                    (info[0],
                    info[1],
                    info[2],
                    info[3],
                    int(info[4])))

    conn.commit()
    cur.close()
    return

def getPopularityAverage():
    conn = sqlite.connect('Spotify.sqlite')
    cur = conn.cursor()

    dict_of_popularity = {}
    average_popularity = []

    cur.execute(''' SELECT popularity, artist_name FROM Spotify''')

    for row in cur:
        popularity = row[0]
        artist = row[1]
        dict_of_popularity[artist] = dict_of_popularity.get(artist, 0) + popularity

    for popularity in dict_of_popularity.items():
        average_popularity.append((popularity[0], (popularity[1])/10))

    return average_popularity

def drawBarChart(average_popularity):
    print('This list shows the average popularity of the top ten tracks of ten artists')
    print(average_popularity)

    plt.xlabel('Artist')
    plt.ylabel('Average Popularity')
    plt.title('Average Popularity of Artist Top Ten Tracks')

    xvals = []
    yvals = []

    for popularity_score in average_popularity:
        xvals.append(popularity_score[0])
        yvals.append(popularity_score[1])

    plt.bar(xvals, yvals, color = 'bgrcmykbgr')
    plt.show()
    return

API = SetUp()
track_info_list = getTopTracks(API, artist_dict)
setUpSpotifyTable(track_info_list)
pop_average_list = getPopularityAverage()
drawBarChart(pop_average_list)
