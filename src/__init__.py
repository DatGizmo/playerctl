#!/usr/bin/python

from src.dbusplayer import DbusPlayer
from src.mpdplayer import MpdPlayer
from src.tasks import Tasks
from src.songdata import SongData
from src.lyricfetcher import LyricFetcher
import getopt
import psutil
import sys

target = None
task = Tasks.NONE
seekTime = 0
songData = None

def printhelp():
    print('playerctrl <option> [--player <player>]')
    print('     options: -P         play')
    print('              -s         stop')
    print('              -n         next')
    print('              -p         prev')
    print('              -t         toggle play/pause')
    print('              -l         Show lyrics for current song')
    print('              -m         get song metadata')
    print('              -M         toggle volume between 0 and 100%')
    print('              -d         decrease volume')
    print('              -i         increase volume')
    print('              --pause ')
    print('              --tmux     print metadata for tmux status')
    print('              --sf       seek forward 30 sec')
    print('              --sb       seek backwards 30 sec')
    print('              --seek=    seek in sec, a leading "-" will seek backwards')
    print('              --artist   set artist for direct lyric search')
    print('              --title    set title for direct lyric search')
    print('              --album    set album for direct lyric search')
    print('              --lyric-fetch fetch lyrics using lyrics fetcher')
    print('              -D         daemon; fetches lyrics and prints to the console')
    print('                                 only works with mpd')
    print('     player:  if player is empty the player is auto detected')
    print('              spotify')
    print('              mpd')

def parscmd(argv):
    global task, target, seekTime, songData, lyricFetcher
    try:
        opts, args = getopt.getopt(argv, "lidhtsnmpa:PDM", ["help", "action=", "player=", "tmux", "sf", "sb", "seek=", "artist=", "title=", "album=", "pause", "lyric-fetch"])
    except getopt.GetoptError:
        printhelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' :
            printhelp()
            sys.exit()
        elif opt == '-t':
            task = Tasks.Toggle
        elif opt == '-s':
            task = Tasks.Stop
        elif opt == '-n':
            task = Tasks.Next
        elif opt == '-p':
            task = Tasks.Prev
        elif opt == '-m':
            task = Tasks.MetaData
        elif opt == '-P':
            task = Tasks.Play
        elif opt == '-d':
            task = Tasks.VolDec
        elif opt == '-i':
            task = Tasks.VolInc
        elif opt == '-l':
            task = Tasks.Lyric
        elif opt == '-D':
            task = Tasks.Daemon
        elif opt == '-M':
            task = Tasks.Mute
        elif opt in ("--help"):
            printhelp()
            sys.exit(0)
        elif opt in ("--pause"):
            task = Tasks.Pause
        elif opt in ("--player"):
            if(arg == 'spotify'):
                target = createSpotify()
            elif(arg == 'mpd'):
                target = createMpd()
            else:
                print("Unkown player")
                printhelp()
                sys.exit(1)
        elif opt in ("--tmux"):
            task = Tasks.Tmux
        elif opt in ("--sf"):
            task = Tasks.SecFwd
        elif opt in ("--sb"):
            task = Tasks.SecBwd
        elif opt in ("--seek"):
            task = Tasks.Seek
            timestr = arg
            inx = timestr.find(":")
            if(inx > 0):
                seekTime = int(timestr[:inx])*60
                seekTime += int(timestr[inx+1:])
            else:
                seekTime = timestr
        elif opt in ("--artist"):
            if songData is None:
                songData = SongData(arg, None, None, None, None, 0, 0)
            else:
                songData.artist = arg
        elif opt in ("--title"):
            if songData is None:
                songData = SongData(None, None, None, arg, None, 0, 0)
            else:
                songData.title = arg
        elif opt in ("--album"):
            if songData is None:
                songData = SongData(None, arg, None, None, None, 0, 0)
            else:
                songData.album= arg
        elif opt in ("--lyric-fetch"):
            lyricFetcher = LyricFetcher(None, None, None)
        else:
            print("Unkown option %s"% opt);
            printhelp()
            sys.exit(1)

def getPids(player):
    pids=[]
    for p in psutil.process_iter():
        if str(player) in str(p.name):
            pids.append(p.pid)
    return sorted(pids)

def getPid(player):
    for p in psutil.process_iter():
        if str(player) in str(p.name):
            return True
    return False

import socket
def testMpdHost():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('MpdHost', 6600))
        return True
    except socket.error as e:
        return False
        #print "Error on connect: %s" % e
    finally:
        s.close()

def getRunningPlayer():
    pids = getPids("mpv")
    if(len(pids) > 0):
        return createMpv(pids)
    elif(getPid("spotify")):
        return createSpotify()
    elif(getPid("Nuvo")):
        print("amazon");
        return createAmazon()
    elif(getPid("mpd") or testMpdHost()):
        return createMpd()
    else:
        return None

def createMpd():
    return MpdPlayer(10, "MpdHost", 6600, "GizmoMpD")

def createSpotify():
    SPOTIFY = 'org.mpris.MediaPlayer2.spotify'
    SPOT_PATH = '/org/mpris/MediaPlayer2'
    pids = []
    return DbusPlayer(SPOTIFY, SPOT_PATH, pids, "Spotify")

def createMpv(pids):
    MPV = 'org.mpris.MediaPlayer2.mpv'
    MPV_PATH = '/org/mpris/MediaPlayer2'
    return DbusPlayer(MPV, MPV_PATH, pids, "mpv")

def createAmazon():
    AMAZON = 'org.mpris.MediaPlayer2.NuvolaOseAppAmazonCloudPlayer'
    AMAZON_PATH = '/org/mpris/MediaPlayer2'
    pids = []
    return DbusPlayer(AMAZON, AMAZON_PATH, pids, "Amazon")

def main(argv):
    global task, songData, target, lyricFetcher
    lyricFetcher = None

    parscmd(argv)
    if(target == None):
        target = getRunningPlayer()

    if(None != lyricFetcher and None != songData):
        lyricFetcher.artist = songData.artist
        lyricFetcher.album = songData.album
        lyricFetcher.title = songData.title
        lyricFetcher.fetchLyrics()
    if(task == Tasks.Lyric and songData != None):
        songData.getLyric()
    elif(target != None):
        target.action(task, seekTime)
    elif(target == None):
        print("No running player found")
        sys.exit(1)

