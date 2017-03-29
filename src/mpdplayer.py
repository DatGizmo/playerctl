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

    def getMetaData(s):
        song = s.mpc.currentsong()
        artist = ''
        album = ''
        track = ''
        title = ''
        td = SongData(artist, album, track, title)
        if 'artist' in song:
            td.artist = song['artist']
        if 'album' in song:
            td.album = song['album']
        if 'track' in song:
            td.track = song["track"]
        if 'title' in song:
            td.title = song['title']
        
        return td

    def metadata(s):
        if(s.mpc.status()['state'] != "play"):
            print("Pause/Stopped")
        else:
            titel = s.getMetaData()
            print titel

    def toggle(s):
        if(s.mpc.status()['state'] != "play"):
            s.mpc.play()
        else:
            s.mpc.pause()

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

    def voldec(self):
        vol = int(s.mpc.status()['volume'])
        s.mpc.setvol(vol-3)

    def seek(s, val):
        s.seekcur(val)
