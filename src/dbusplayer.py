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
        s.status = s.mplayer.player.PlaybackStatus
        s.name = n

    def playing(s):
        return ('play' in s.status.lower())

    def classname(s):
        return s.name

    def getSongData(s):
        song = s.mplayer.player.Metadata
        td = SongData('', '', '', '', '', 0, 0)
        if 'xesam:artist' in song:
            td.artist = song['xesam:artist'][0]
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
        s.iface.PlayPause()

    def play(s):
        s.iface.Play()

    def pause(s):
        s.iface.Pause()

    def next(s):
        s.iface.Next()

    def prev(s):
        s.iface.Previous()

    def stop(s):
        s.iface.Stop()

    def volinc(self):
        pass

    def voldec(self):
        pass

    def seek(self, vol):
        pass

