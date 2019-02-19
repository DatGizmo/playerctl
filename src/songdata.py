import requests
from datetime import datetime
from lyricsmaster import Genius
from os.path import expanduser
from os import path

class SongData(object):
    def __init__(self, artist, album, track, title, fn, length, elapsed):
        self.artist = artist
        self.album = album
        self.track = track
        self.title = title
        self.lyric = ''
        self.filename = fn
        self.length = length
        self.elapsed = elapsed

    def __str__(self):
        retval = ''
        if self.artist:
            retval += self.artist + " - "
        if self.album:
            retval += self.album + " - "
        if self.track:
            retval += str(self.track) + "."
        if self.title:
            retval += self.title
        if not retval:
            retval = self.filename
        if self.elapsed != 0:
            retval += " - " + datetime.fromtimestamp(self.elapsed).strftime('%M:%S')
        if self.length:
            if self.elapsed == 0:
                retval += " - "
            else:
                retval += "/"
            retval += datetime.fromtimestamp(self.length).strftime('%M:%S')

        return retval

    def toString(self):
        return self.__str__()
    
    def fetchLyric(self):
        provider = Genius()
        song = provider.get_lyrics(self.artist)
        data.save()
        getLyricFromFile()

    def getLyricFromFile(self):
        dirs = path.join(expanduser("~"), "Documents/LyricsMaster/", self.artist).replace(' ', '-')
        if path.exists(dirs):
            albump = path.join(dirs, self.album).replace(' ', '-')
            if path.exists(albump):
                lyricp = path.join(albump, self.title + '.txt').replace(' ', '-')
                print(lyricp)
                if path.exists(lyricp):
                    print("Blub")
                    fp = open(lyricp)
                    self.lyric = fp.read()
                    fp.close()

    def fetchFromMIP(self): 
        payload = {'artist': self.artist, 'title': self.title}
        r = requests.get('https://makeitpersonal.co/lyrics', params = payload)
        self.lyric = r.text
        #save to file

    def getLyric(self):
        if not self.lyric:
            self.getLyricFromFile()
        if not self.lyric:
            self.fetchFromMIP()
        if not self.lyric:
            self.fetchLyric()

        if self.lyric[0] == '\n':
            self.lyric = self.lyric[1:len(self.lyric)]
        if self.lyric[len(self.lyric)-1] == '\n':
            self.lyric = self.lyric[0:len(self.lyric)-1]

        print(self)
        print(self.lyric)

