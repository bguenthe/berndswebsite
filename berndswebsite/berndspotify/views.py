import json

from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from spotipy import util


def index(request):
    onames = get_saved_albums()

    return HttpResponse(onames)

def get_saved_albums():
    scope = 'user-library-read'
    token = util.prompt_for_user_token("bguenthe", scope, "edff16eb5b2c4602bd3cc3c0ac551e3d", "84c6d9d3637f4882bf36119337089c64", "http://www.heise.de")

    spotify = spotipy.Spotify(auth=token)

    first = True
    onames = []
    while True:
        if first:
            results = spotify.current_user_saved_albums(limit=20, offset=0)
            first = False
        else:
            results = spotify.next(results)

        if results != None:
            items = results["items"]
            for album in items:
                onames.append(album["album"]['name'] + "<br>")
        else:
            break

    return onames

def get_followed_artists():
    scope = 'user-follow-read'
    token = util.prompt_for_user_token("bguenthe", scope, "edff16eb5b2c4602bd3cc3c0ac551e3d", "84c6d9d3637f4882bf36119337089c64", "http://www.heise.de")

    spotify = spotipy.Spotify(auth=token)

    # liest nur 20!
    results = spotify.current_user_followed_artists(limit=20, after=None)
    after = results['artists']["cursors"]["after"]
    names = results['artists']["items"]
    onames = []
    for name in names:
        onames.append(name['name'] + "<br>")

    return onames

# def index(request):
#     scope = 'user-library-read'
#     #token = util.prompt_for_user_token("bernd.stuebe@googlemail.com", scope, "edff16eb5b2c4602bd3cc3c0ac551e3d", "84c6d9d3637f4882bf36119337089c64", "localhost:8000/berndspotifyredirect")
#     #auth = spotipy.oauth2.SpotifyClientCredentials(client_id="edff16eb5b2c4602bd3cc3c0ac551e3d", client_secret="84c6d9d3637f4882bf36119337089c64")
#     auth = spotipy.oauth2.SpotifyOAuth(client_id="edff16eb5b2c4602bd3cc3c0ac551e3d", client_secret="84c6d9d3637f4882bf36119337089c64", redirect_uri="http://www.heise.de", state=None, scope=None, cache_path="d")
#     url = auth.get_authorize_url()
#
#     code = auth.parse_response_code(url)
#     token = auth.get_access_token(code)
#
#     #token = auth.get_access_token()
#     #token = auth.get_cached_token()
#
#     spotify = spotipy.Spotify(token)
#     results = spotify.current_user_followed_artists(limit=20, after=None)
#
#     return HttpResponse(results)
