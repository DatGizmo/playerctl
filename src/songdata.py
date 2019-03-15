import requests
from datetime import datetime
from lyricsmaster import Genius
from lyricsmaster import LyricWiki
from os.path import expanduser
from os import path
from os import makedirs
from os import walk
from os import removedirs
from shutil import move

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
        self.lyricroot = path.join(expanduser("~"), "Documents/LyricsMaster/")
        self.artistroot = ''
        self.albumroot = ''
        self.lyricspath = ''

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

    def setPaths(self):
        self.artistroot = path.join(self.lyricroot, self.artist).replace(' ', '-')
        self.albumroot = path.join(self.artistroot, self.album).replace(' ', '-')
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

    def checkFileExists(self, create=False):
        fpexists = False
        if(self.checkFolderExists(create)):
            if path.exists(self.lyricspath):
                fpexists = True
        if(not fpexists and self.searchFolder()):
            fpexists = True
        return fpexists

    def fetchFromProvider(self, provider):
        if provider:
            data = provider.get_lyrics(self.artist)
            if data:
                data.save()

    def fetchLyric(self):
        print("Fetching artists lyrics with lyricsmaster using Genius")
        self.fetchFromProvider(Genius())
        if(not self.checkFileExists()):
            print("Fetching artists lyrics with lyricsmaster using LyricWiki")
            self.fetchFromProvider(LyricWiki())
            if(not self.checkFileExists()):
               return
        if(self.title):
            self.getLyricFromFile()

    def getLyricFromFile(self):
        fp = open(self.lyricspath)
        self.lyric = fp.read()
        fp.close()

    def fetchFromMIP(self):
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

    def searchFolder(self):
        result = []
        retval = False
        fileName = self.title.replace(' ', '-') + ".txt"
        for root, dirs, files in walk(self.lyricroot):
            for fp in files:
                if fileName.lower() in fp.lower():
                    result.append(path.join(root, fp))
        if len(result) >= 1:
            self.lyricspath = result[0]
            self.getLyricFromFile()
            retval = True
        else:
            print("Could not find file with lyrics for \"%s\"" % self.title)
        return retval

    def getLyric(self, nofetch):
        if self.title and (not self.artist or not self.album):
            self.searchFolder()
        elif(not nofetch and self.artist and not self.title and not self.album):
            self.fetchLyric()
            return
        elif(self.checkFileExists()):
            if not self.lyric:
                self.getLyricFromFile()
        if not nofetch and self.title and self.artist and not self.lyric:
            self.fetchFromMIP()
        if not nofetch and self.artist and not self.lyric:
            self.fetchLyric()

        if self.lyric:
            if self.lyric[1] == '\n':
                self.lyric = self.lyric[2:len(self.lyric)]
            if self.lyric[len(self.lyric)-1] == '\n':
                self.lyric = self.lyric[0:len(self.lyric)-1]

            print(self)
            if self.lyric[0] != '\n':
                print()
            print(self.lyric)

