from src.player import Player
import dbus
import pympris
from src.songdata import SongData

class DbusPlayer(Player):
    def __init__(s, dest, path, ifacen, n):
        s.bus = dbus.SessionBus()
        s.obj = s.bus.get_object(dest, path)
        s.iface = dbus.Interface(s.obj, dbus_interface=ifacen)
        players_ids = list(pympris.available_players())
        s.mplayer = pympris.MediaPlayer(players_ids[0], s.bus)
        s.player = s.mplayer.player
        s.status = s.mplayer.player.PlaybackStatus
        s.name = n

    def playing(s):
        return ('play' in s.status.lower())

    def paused(s):
        return ('pause' in s.status.lower())

    def classname(s):
        return s.name

    def getSongData(s):
        song = s.mplayer.player.Metadata
        td = SongData(None, None, None, None, None, 0, 0)
        if 'xesam:artist' in song:
            artist = str(song['xesam:artist'])
            td.artist = (artist[2:len(artist)-2])
        if 'xesam:album' in song:
            td.album = song['xesam:album']
        if 'xesam:trackNumber' in song:
            td.track = song['xesam:trackNumber']
        if 'xesam:title' in song:
            td.title = song['xesam:title']
        if 'mpris:length' in song:
            td.length = song['mpris:length']/1000/1000

        return td

    def toggle(s):
        s.player.PlayPause()

    def play(s):
        s.player.Play()

    def pause(s):
        s.player.Pause()

    def next(s):
        s.player.Next()

    def prev(s):
        s.player.Previous()

    def stop(s):
        s.player.Stop()

    def volinc(s):
        if( s.name != "Spotify" ):
            s.player.Volume = s.player.Volume + 3/100
        else:
            pass

    def voldec(s):
        if( s.name != "Spotify" ):
            s.player.Volume = s.player.Volume - 3/100
        else:
            pass

    def seek(s, val):
        if( s.player.CanSeek ):
            seeker = int(val) * 1000 * 1000
            s.player.Seek(seeker)
        else:
            pass

