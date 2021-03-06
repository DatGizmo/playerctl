from abc import ABCMeta, abstractmethod
from src.tasks import Tasks
import math
import datetime

class Player:
    __metaclass__ = ABCMeta

    @abstractmethod
    def toggle(self):
        pass

    @abstractmethod
    def getSongData(self):
        pass

    def metadata(self):
        if self.playing():
            print(self.getSongData())
        elif self.paused():
            print(self.classname() + ": Paused")
        else:
            print(self.classname() + ": Stopped")

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def prev(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def volinc(self):
        pass

    @abstractmethod
    def voldec(self):
        pass

    @abstractmethod
    def mute(self):
        pass

    @abstractmethod
    def seek(self, vol):
        pass

    @abstractmethod
    def playing(self):
        pass

    @abstractmethod
    def paused(self):
        pass

    @abstractmethod
    def classname(self):
        pass

    def lyric(s):
        sd = s.getSongData()
        sd.getLyric()

    def tmux(s):
        printstr=""
        maxlen = 40
        mod = 15
        pause_stop = ": Stopped"
        if s.paused():
            pause_stop = ": Paused"
        titel = s.classname() + pause_stop
        if s.playing():
            titel = s.getSongData().toString()
        length = len(titel)
        steps = int(math.ceil((float(length)+3)/mod))

        if length > maxlen:
            now = datetime.datetime.now()
            start = now.second % mod
            start *= steps
            if start >= length:
                start = 0
            end = start + maxlen
            if end > length:
                end = length

            printstr = titel[start:end]
            prlen = len(printstr)
            if(prlen < maxlen):
                printstr = printstr + " | " + titel[0:(maxlen-prlen)]
                printstr = printstr[0:maxlen]
            print(printstr)
        else:
            print(titel)

    def action(s, task, seekTime):
        if(task == Tasks.Daemon):
            #runDaemon()
            pass
        elif(task == Tasks.Play):
            s.play()
        elif(task == Tasks.Pause):
            s.pause()
        elif(task == Tasks.Stop):
            s.stop()
        elif(task == Tasks.Next):
            s.next()
        elif(task == Tasks.Prev):
            s.prev()
        elif(task == Tasks.Toggle):
            s.toggle()
        elif(task == Tasks.VolInc):
            s.volinc()
        elif(task == Tasks.VolDec):
            s.voldec()
        elif(task == Tasks.SecBwd):
            s.seek("-30")
        elif(task == Tasks.SecFwd):
            s.seek("+30")
        elif(task == Tasks.Seek):
            s.seek(seekTime)
        elif(task == Tasks.MetaData):
            s.metadata()
        elif(task == Tasks.Tmux):
            s.tmux()
        elif(task == Tasks.Lyric):
            s.lyric()
        elif(task == Tasks.Mute):
            s.mute()

