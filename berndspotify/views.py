import json
import operator
import locale

import sys
from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from spotipy import util

def normalizeSortString(s):
    return locale.strxfrm(s)

def getSortKey(k):
    return (normalizeSortString(k['artist']), normalizeSortString(k["album"]))

def index(request):
    onames = get_saved_albums()

    return HttpResponse(onames)

def get_saved_albums():
    platform = sys.platform
    if platform == "win32":
        locale.setlocale(locale.LC_ALL, 'deu_deu')
    else:
        locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

    scope = 'user-library-read'
    token = util.prompt_for_user_token("bguenthe", scope, "edff16eb5b2c4602bd3cc3c0ac551e3d", "84c6d9d3637f4882bf36119337089c64", "http://www.heise.de")

    spotify = spotipy.Spotify(auth=token)

    onames = []
    info = {}
    results = spotify.get_all_current_user_saved_albums()

    for album in results:
        info = {}
        info["album"] = album["album"]['name']
        info["artist"] = album["album"]['artists'][0]["name"]
        info["image"] = album["album"]['images'][0]["url"]
        info["added_at"] = album['added_at']
        onames.append(info)

    onames.sort(key=getSortKey)

    html = """<table style="width:100%">"""
    for oname in onames:
        html += "<tr>"
        html += "<td>" + oname["artist"] + "</td>"
        html += "<td>" + oname["album"] + "</td>"
        html += "<td>" + oname["added_at"] + "</td>"
        html += '<td><img src="' + oname['image'] + '"' + 'style="width:100px;height:100    px;"></td>'
        html += "</tr>"

    html += "</table>"
    return HttpResponse(html)

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

