from src.player import Player
import dbus
import pympris
from src.songdata import SongData

class DbusPlayer(Player):
    def __init__(s, dest, path, pids, n):
        PID_DEST = "org.freedesktop.DBus"
        PID_PATH = "/"
        PID_IFACE = PID_DEST

        bus = dbus.SessionBus()
        pidObj = bus.get_object(PID_DEST, PID_PATH)
        pidIface = dbus.Interface(pidObj, PID_IFACE)
        s.players = []

        if(len(pids) > 1):
            for e in bus.list_names():
                if dest in e:
                    pid = pidIface.GetConnectionUnixProcessID(e)
                    if pid in pids:
                        s.players.append(pympris.MediaPlayer(e).player)
                        pids.remove(pid)
        else:
            s.players.append(pympris.MediaPlayer(dest).player)

        players_ids = list(pympris.available_players())
        s.name = n

    @property
    def Player(s):
        # Get the first player (lowest pid) when we don't want to acess all players
        if(len(s.players) > 0):
            return s.players[0]

    def playing(s):
        return ('play' in s.Player.PlaybackStatus.lower())

    def paused(s):
        return ('pause' in s.Player.PlaybackStatus.lower())

    def classname(s):
        return s.name

    def getSongData(s):
        song = s.Player.Metadata
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
        for p in s.players:
            p.PlayPause()

    def play(s):
        s.Player.Play()

    def pause(s):
        s.Player.Pause()

    def next(s):
        s.Player.Next()

    def prev(s):
        s.Player.Previous()

    def stop(s):
        s.Player.Stop()

    def volinc(s):
        if( s.name != "Spotify" ):
            s.Player.Volume = s.Players.Volume + 3/100
        else:
            pass

    def voldec(s):
        if( s.name != "Spotify" ):
            s.Player.Volume = s.Players.Volume - 3/100
        else:
            pass

    def seek(s, val):
        if( s.Player.CanSeek ):
            seeker = int(val) * 1000 * 1000
            s.Player.Seek(seeker)
        else:
            pass

