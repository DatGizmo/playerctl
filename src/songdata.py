import requests
from datetime import datetime
from os.path import expanduser
from os import path
from os import makedirs
from os import walk
from os import removedirs
from shutil import move
import re

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
            form='%M:%S'
            if(60 < (self.elapsed/60)):
                form='%H:%M:%S'
            retval += " - " + datetime.utcfromtimestamp(self.elapsed).strftime(form)
        if self.length:
            form='%M:%S'
            if(60 < (self.length/60)):
                form='%H:%M:%S'
            if self.elapsed == 0:
                retval += " - "
            else:
                retval += "/"
            retval += datetime.utcfromtimestamp(self.length).strftime(form)

        return retval

    def toString(self):
        return self.__str__()

    def setPaths(self):
        if(self.artist):
            self.artistroot = path.join(self.lyricroot, self.artist).replace(' ', '-')
        if(self.album):
            self.albumroot = path.join(self.artistroot, self.album).replace(' ', '-')
        if(self.title):
            self.lyricspath = path.join(self.albumroot, self.title + '.txt').replace(' ', '-')

    def checkFolderExists(self):
        exists = False
        if(not self.album or not self.artist):
            return self.searchFolder()
        self.setPaths()
        if path.exists(self.artistroot):
            if path.exists(self.albumroot):
                exists = True
        return exists

    def checkFileExists(self):
        fpexists = False
        if(self.checkFolderExists()):
            if path.exists(self.lyricspath):
                fpexists = True
        if(not fpexists and self.searchFolder()):
            fpexists = True
        return fpexists

    def getLyricFromFile(self):
        fp = open(self.lyricspath)
        self.lyric = fp.read()

        if self.lyric[1] == '\n':
            self.lyric = self.lyric[2:len(self.lyric)]
        if self.lyric[len(self.lyric)-2] == '\n' and self.lyric[len(self.lyric)-1] == '\n':
            self.lyric = self.lyric[0:len(self.lyric)-1]

        self.lyric += '\n'
        pos = self.lyricspath.find("LyricsMaster") + len("LyricsMaster/")
        self.lyric += self.lyricspath[pos:len(self.lyricspath)]
        fp.close()

    def searchFolder(self):
        result = []
        retval = False
        reg = re.compile(r"(\([\d]*\))|[\(\)\!]")
        trailing = re.compile(r"[\s]$")
        fileName = reg.sub("", self.title)
        fileName = trailing.sub("", fileName)
        fileName = fileName.replace(' ', '-') + ".txt"
        print(fileName)
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

    def getLyric(self):
        if self.title and (not self.artist or not self.album):
            self.searchFolder()
        elif(self.title and self.checkFileExists()):
            if not self.lyric:
                self.getLyricFromFile()

        if self.lyric:
            print(self)
            if self.lyric[0] != '\n':
                print()
            print(self.lyric)

