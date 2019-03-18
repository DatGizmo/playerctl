import requests
from datetime import datetime
from lyricsmaster.providers import Genius
from lyricsmaster.providers import LyricWiki
from lyricsmaster.providers import MusixMatch
from lyricsmaster.providers import AzLyrics
from os.path import expanduser
from os import path
from os import makedirs
from os import walk
from os import removedirs
from shutil import move

class LyricFetcher(object):
    def __init__(self, artist, album, title):
        self.artist = artist
        self.album = album
        self.title = title
        self.lyricroot = path.join(expanduser("~"), "Documents/LyricsMaster/")
        self.artistroot = ''
        self.albumroot = ''
        self.lyricspath = ''

    def setPaths(self):
        if(self.artist):
            self.artistroot = path.join(self.lyricroot, self.artist).replace(' ', '-')
        if(self.album):
            self.albumroot = path.join(self.artistroot, self.album).replace(' ', '-')
        if(self.title):
            self.lyricspath = path.join(self.albumroot, self.title + '.txt').replace(' ', '-')

    def checkFolderExists(self, create=False):
        exists = False
        if(not self.album or not self.artist):
            return self.searchFolder()
        self.setPaths()
        if path.exists(self.artistroot):
            if path.exists(self.albumroot):
                exists = True
        if(False == exists and True == create):
            makedirs(path.join(self.lyricroot, self.artist, self.album).replace(' ', '-'))
            exists = True
        return exists

    def fetchFromProvider(self, provider):
        try:
            print()
            print("Fetching artists lyrics with lyricsmaster using %s" % provider.name)
            if provider:
                data = provider.get_lyrics(self.artist, self.album, self.title)
                if data:
                    data.save()
        except:
            print("ToDo proper error handling")
            pass

    def fetchFromMIP(self):
        if(not self.title or not self.album):
            return
        print("Fetching with MIP")
        payload = {'artist': self.artist, 'title': self.title}
        r = requests.get('https://makeitpersonal.co/lyrics', params = payload)
        if("Sorry, We don't have lyrics for this song yet" not in r.text):
            self.lyric = r.text
            if(self.album):
                self.checkFolderExists(True)
                fp = open(self.lyricspath, 'w+')
                fp.write(self.lyric)
                fp.close()

    def fetchLyrics(self):
        self.fetchFromMIP()
        self.fetchFromProvider(Genius())
        self.fetchFromProvider(LyricWiki())
#        self.fetchFromProvider(MusixMatch())
        self.fetchFromProvider(AzLyrics())

