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
        self.artistroot = path.join(self.lyricroot, self.artist.lower()).replace(' ', '-')
        self.albumroot = path.join(self.artistroot, self.album.lower()).replace(' ', '-')
        self.lyricspath = path.join(self.albumroot, self.title.lower() + '.txt').replace(' ', '-')

    def checkFileExists(self, create=False):
        exists = False
        if(not self.album or not self.artist):
            return self.searchFolder()
        self.setPaths()
        print(self.artistroot)
        if path.exists(self.artistroot):
            print(self.albumroot)
            if path.exists(self.albumroot):
                print(self.lyricspath)
                if path.exists(self.lyricspath):
                    print("True")
                    exists = True
        if(False == exists and True == create):
            makedirs(path.join(self.lyricroot, self.artist.lower(), self.album.lower()).replace(' ', '-'))
            exists = True
        if(not exists and self.searchFolder()):
            exists = True
        return exists

    def fetchFromProvider(self, provider):
        if provider:
            data = provider.get_lyrics(self.artist)
            data.save()
            # Move all to lower case version
            for root, dirs, files in walk(self.lyricroot):
                for dr in dirs:
                    if self.artist.lower().replace(' ', '-') in dr.lower():
                        artsrc = dr
                        artdest = dr.lower()
                        if(not path.exists(path.join(root, artdest))):
                            move(path.join(root, artsrc), path.join(root, artdest))
                            artsrc = artdest
                        for root2, dirs2, files2 in walk(path.join(root, artsrc)):
                            for drr in dirs2:
                                albumsrc = drr
                                albumdest = drr.lower()
                                if(not path.exists(path.join(root, artdest, albumdest))):
                                    move(path.join(root2,  albumsrc), path.join(root, artdest, albumdest))
                                    albumsrc = albumdest
                                    print(albumsrc)
                                for root3, dirs3, files3 in walk(path.join(root, artsrc, albumsrc)):
                                    for fp in files3:
                                        move(path.join(root3, fp), path.join(root, artdest, albumdest, fp.lower()))
                                rmalbump = path.join(root, dr, drr)
                                if(path.exists(rmalbump)):
                                    try:
                                        removedirs(rmalbump)
                                    except OSError:
                                        pass
                            rmartp = path.join(root, dr)
                            if(path.exists(rmartp)):
                                try:
                                    removedirs(path.join(root, dr)) 
                                except OSError:
                                    pass

    def fetchLyric(self):
        print("Fetching artists lyrics with lyricsmaster using Genius")
        self.fetchFromProvider(Genius())
        if(not self.checkFileExists()):
            self.getLyricFromFile()
#           print("Fetching artists lyrics with lyricsmaster using LyricWiki")I
#            self.fetchFromProvider(LyricWiki())
#            if(not self.checkFileExists()):
#               return 


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
                self.checkFileExists(True)
                fp = open(self.lyricspath, 'w+')
                fp.write(self.lyric)
                fp.close()

    def searchFolder(self):
        result = []
        retval = False
        fileName = self.title.replace(' ', '-') + ".txt"
        for root, dirs, files in walk(self.lyricroot):
            if fileName.lower() in files:
                result.append(path.join(root, fileName.lower()))
        if len(result) >= 1:
            self.lyricspath = result[0]
            self.getLyricFromFile()
            retval = True
        else:
            print("Could not find file with lyrics for \"%s\"" % self.title)
        return retval

    def getLyric(self):
        if self.title and not self.artist or not self.album:
            self.searchFolder()
        elif(self.checkFileExists()):
            if not self.lyric:
                self.getLyricFromFile()
        if self.title and self.artist and not self.lyric:
            self.fetchFromMIP()
        if self.artist and not self.lyric:
            self.fetchLyric()

        if self.lyric:
            if self.lyric[1] == '\n':
                self.lyric = self.lyric[2:len(self.lyric)]
            if self.lyric[len(self.lyric)-1] == '\n':
                self.lyric = self.lyric[0:len(self.lyric)-1]

            print(self)
            print(self.lyric)

