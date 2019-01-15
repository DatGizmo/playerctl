import requests
from datetime import datetime

class SongData(object):
    def __init__(self, artist, album, track, title, fn, length):
        self.artist = artist
        self.album = album
        self.track = track
        self.title = title
        self.lyric = ''
        self.filename = fn
        self.lenght = length

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
        if self.length:
            retval +=  " - " + datetime.fromtimestamp(self.length).strftime('%M:%S')

        return unicode(retval)

    def toString(self):
        return self.__str__()

    def getLyric(self):
        if not self.lyric:
            payload = {'artist': self.artist, 'title': self.title}
            r = requests.get('https://makeitpersonal.co/lyrics', params = payload)
            self.lyric = r.text
            if self.lyric[0] == '\n':
                self.lyric = self.lyric[1:len(self.lyric)]
            if self.lyric[len(self.lyric)-1] == '\n':
                self.lyric = self.lyric[0:len(self.lyric)-1]

        print self
        print ""
        print self.lyric

