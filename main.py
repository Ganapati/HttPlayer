#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from bottle import Bottle, run, view, static_file, request
import os, fnmatch
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen import File
import base64
import json

app = Bottle()
files = []
artists = []
genres = []
root = "./sample/"
scanned = False

###        ###
# APP ROUTES #
###        ###

@app.route("/", method='GET')
@view("index.tpl")
def index():
	return {}

@app.route("/getSongs", method='POST')
def getSongs():
	filter = request.forms.get("filter")
	artist = request.forms.get("artist")
	genre = request.forms.get("genre")

	musics = []
	global scanned
	for file in files:
		index = file["index"]
		file = file["file"]
		filename = file.replace(root, "")
		filename = filename.replace(" ", "%20")
		mp3file = MP3(file, ID3=EasyID3)
		infos = getTagsInfos(mp3file)

		
		if scanned == False:
			if infos["genre"] not in genres:
				genres.append(infos["genre"])
			if [infos["artist"], infos["genre"]] not in artists:
				artists.append([infos["artist"], infos["genre"]])

		if artist != "" and infos["artist"] != artist:
			continue

		if genre != "" and infos["genre"] != genre:
			continue

		if not filter.lower() in infos["artist"].lower() and not filter.lower() in infos["title"].lower() and not filter.lower() in infos["album"].lower() and not filter.lower() in infos["genre"].lower():
			continue

		musics.append({	'file'		: filename, 
						'artist'	: infos["artist"],
						'title'		: infos["title"],
						'album'		: infos["album"],
						'genre'		: infos["genre"],
						'index'		: index
					 })
	scanned = True
	data = {"files": musics}
	return data

@app.route('/getInfos', method='POST')
def getInfos():
	index		= request.forms.get('index')
	file		= files[int(index)]["file"]
	mp3file		= MP3(file, ID3=EasyID3)
	cover		= File(file)
	art 		= ""
	mime		= ""
	if "APIC:" in cover:
		art			= base64.b64encode( cover["APIC:"].data )
		mime		= cover["APIC:"].mime
	response	= {'file': file.replace(root, "").replace(" ", "%20"), 'infos': getTagsInfos(mp3file), "art": art, "mime": mime}
	return response

@app.route('/getGenres', method='GET')
def getGenres():
	return json.dumps(genres)

@app.route('/getArtists', method='GET')
def getArtists():
	return json.dumps(artists)

@app.route('/static/<filename:path>')
def serve_static(filename):
	return static_file(filename, root='./static/')

@app.route('/file/<filename:path>')
def serve_file(filename):
	if filename[-4:] == ".mp3":
		filename = filename.replace("%20", " ")
		return static_file(filename, root)
	
###  ###
# CORE #
###  ###

def getTagsInfos(mp3file):
	album = "unknown"
	if 'album' in mp3file:
		album = str(mp3file['album'][0].encode("utf-8"))
	artist = "unknown"
	if 'artist' in mp3file:
		artist = str(mp3file['artist'][0].encode("utf-8"))
	genre = "unknown"
	if 'genre' in mp3file:
		genre = str(mp3file['genre'][0].encode("utf-8"))
	title = "unknown"
	if 'title' in mp3file:
		title = str(mp3file['title'][0].encode("utf-8"))
	return {'album': album, 'artist':artist, 'genre':genre, 'title':title}	

def main(commands, files):
	files += recursive_glob(commands.path, "*.mp3") 
	app.run(server='cherrypy', host='0.0.0.0', port=int(commands.port), reloader=True, debug=True)

def recursive_glob(treeroot, pattern):
	results = []
	for base, dirs, files in os.walk(treeroot):
		goodfiles = fnmatch.filter(files, pattern)
		results.extend(os.path.join(base, f) for f in goodfiles)
	
	f = []
	index = 0
	for r in results:
		f.append({"index": index, "file": r})
		index = index + 1
	return f

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-P", action="store", dest="path", help="path to your music", default="./sample/")
	parser.add_argument("-p", action="store", dest="port", help="listening port", default="1337")
	commands = parser.parse_args()
	root = commands.path
	main(commands, files)
