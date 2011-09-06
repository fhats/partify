from mpd import MPDClient

class mpd_client(object):
    def __init__(self, host="ubuntu.local", port=6600):
        self.host = host
        self.port = port
        self.c = MPDClient()
        self.c.connect(host=self.host, port=self.port)
    
    def __del__(self):
        self.c.disconnect()
    
    def __enter__(self):
        return self.c
    
    def __exit__(self, type, value, traceback):
        if type is not None:
            raise Exception("%s,%s,%s" % (type, value, traceback))

    def play(self):
        self.c.play()

    def pause(self):
        self.c.pause()

    def next(self):
        self.c.next()

    def previous(self):
        self.c.previous()
    
    def status(self):
        return self.c.status()

    def currentsong(self):
        return self.c.currentsong()
