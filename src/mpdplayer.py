from player import Player
from songdata import SongData
from mpd import MPDClient

class MpdPlayer(Player):
    def __init__(s, timeout, host, port, passwd):
        s.mpc = MPDClient()
        s.mpc.timeout = timeout
        s.mpc.idletimeout = None
        s.mpc.connect(host, port)
        s.mpc.password(passwd)

    def playing(s):
        return (s.mpc.status()['state'] == "play")

    def classname(s):
        return "MPD"

    def getSongData(s):
        song = s.mpc.currentsong()
        td = SongData('', '', '', '', '')
        if 'artist' in song:
            td.artist = song['artist']
        if 'album' in song:
            td.album = song['album']
        if 'track' in song:
            td.track = song['track']
        if 'title' in song:
            td.title = song['title']
        if 'file' in song:
            name = song['file']
            pos = name.rfind('/')
            if pos > 0:
                td.filename = name[pos+1:]
            else:
                td.filename = name
        
        return td

    def toggle(s):
        if(s.playing()):
            s.mpc.pause()
        else:
            s.mpc.play()

    def play(s):
        s.mpc.play()

    def pause(s):
        s.mpc.pause()

    def next(s):
        s.mpc.next()

    def prev(s):
        s.mpc.previous()

    def stop(s):
        s.mpc.stop()

    def volinc(s):
        vol = int(s.mpc.status()['volume'])
        s.mpc.setvol(vol+3)

    def voldec(s):
        vol = int(s.mpc.status()['volume'])
        s.mpc.setvol(vol-3)

    def seek(s, val):
        s.mpc.seekcur(val)

