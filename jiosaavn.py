import requests
import endpoints
import helper
import json
from traceback import print_exc
from urllib.parse import urlparse
from requests.compat import urljoin

def search_for_song(query,lyrics,songdata):
    if query.startswith('http') and 'saavn.com' in query:
        id = get_song_id(query)
        return get_song(id, lyrics)

    search_base_url = endpoints.search_base_url+query
    response = requests.get(search_base_url).text.encode().decode('unicode-escape')
    response = json.loads(response)
    song_response = response['songs']['data']
    if not songdata:
        return song_response
    songs = []
    for song in song_response:
        id = song['id']
        song_data = get_song(id, lyrics)
        if song_data:
            songs.append(song_data)
    return songs

def get_song(id,lyrics):
    try:
        song_details_base_url = endpoints.song_details_base_url+id
        song_response = requests.get(song_details_base_url).text.encode().decode('unicode-escape')
        song_response = json.loads(song_response)
        song_data = helper.format_song(song_response[id],lyrics)
        if song_data:
            return song_data
    except:
        return None

def get_song_id(url):
    res = requests.get(url, data=[('bitrate', '320')])
    try:
        return res.text.split('"song":{"type":"')[1].split('","image":')[0].split('"id":"')[-1]
    except IndexError:
        return(res.text.split('"pid":"'))[1].split('","')[0]

def get_album(album_id,lyrics):
    songs_json = []
    try:
        response = requests.get(endpoints.album_details_base_url+album_id)
        if response.status_code == 200:
            songs_json = response.text.encode().decode('unicode-escape')
            songs_json = json.loads(songs_json)
            return helper.format_album(songs_json,lyrics)
    except Exception as e:
        print(e)
        return None

def get_album_id(input_url):
    res = requests.get(input_url)
    try:
        return res.text.split('"album_id":"')[1].split('"')[0]
    except IndexError:
        return res.text.split('"page_id","')[1].split('","')[0]

def get_playlist(listId,lyrics):
    try:
        response = requests.get(endpoints.playlist_details_base_url+listId)
        if response.status_code == 200:
            songs_json = response.text.encode().decode('unicode-escape')
            songs_json = json.loads(songs_json)
            return helper.format_playlist(songs_json,lyrics)
        return None
    except Exception:
        print_exc()
        return None

def get_playlist_id(input_url):
    your_url = input_url
    final_url = urlparse(urljoin(your_url, "/"))
    is_correct = (all([final_url.scheme, final_url.netloc, final_url.path]) 
              and len(final_url.netloc.split(".")) > 1)
    if is_correct:
        res = requests.get(input_url).text
        try:
            if '"type":"playlist","id":"' in res:
                return res.split('"type":"playlist","id":"')[1].split('"')[0]
            else:
                return input_url   
            return res.split('"type":"playlist","id":"')[1].split('"')[0]
        except IndexError:
            return res.split('"page_id","')[1].split('","')[0]
    else:
        return input_url

def get_lyrics(id):
    url = endpoints.lyrics_base_url+id
    lyrics_json = requests.get(url).text
    lyrics_text = json.loads(lyrics_json)
    return lyrics_text['lyrics']

def get_embed_url(id):
    if id.isnumeric():
        response = {
            "status": True,
            "embed_base_url":endpoints.embed_base_url+id
        }
        #response = [("embed_base_url",endpoints.embed_base_url+id)]
        embed_json = response
    else:
        embed_json = {
            "status": False,
            "error":'Not valid Playlist!'
        }
        #embed_json = [("embed_base_url","Not valid Playlist")]
    return embed_json