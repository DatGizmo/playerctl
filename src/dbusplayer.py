from player import Player
import dbus
import pympris
from songdata import SongData

class DbusPlayer(Player):
    def __init__(s, dest, path, ifacen):
        s.bus = dbus.SessionBus()
        s.obj = s.bus.get_object(dest, path)
        s.iface = dbus.Interface(s.obj, dbus_interface=ifacen)
        players_ids = list(pympris.available_players())
        s.mplayer = pympris.MediaPlayer(players_ids[0], s.bus)
        s.status = s.mplayer.player.PlaybackStatus

    def getMetaData(s):
        return SongData(s.mplayer.player.Metadata['xesam:artist'][0], s.mplayer.player.Metadata['xesam:album'], str(s.mplayer.player.Metadata['xesam:trackNumber']), s.mplayer.player.Metadata['xesam:title'])

    def metadata(s):
        if 'play' in s.status.lower():
            titel = s.getMetaData()
            print(titel)
        else:
            print("Pause/Stopped")
        
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

    def lyric(self):
        pass

 
