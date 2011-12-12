# Copyright 2011 Fred Hatfull
#
# This file is part of Partify.
#
# Partify is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Partify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Partify.  If not, see <http://www.gnu.org/licenses/>.

import time
from multiprocessing import Event, Manager, Queue

from partify import ipc
from partify.models import PlayQueueEntry
from testing.data.sample_tracks import sample_tracks
# Be careful with this...
try:
    idle_event_queue
except NameError:
    idle_event_queue = Queue()

try:
    manager
except NameError:
    print "Create manager"
    manager = Manager()

try:
    idle_event
except NameError:
    idle_event = Event()


class MockMPDClient(object):
    """A mock MPD client which does not actually connect to an MPD server but acts like it does."""

    instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(MockMPDClient, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    connected = False

    track_list = []

    state = "play"

    def send_idle(self):
        global idle_event
        idle_event.set()
        idle_event.clear()
    
    def stop_idle(self):
        global idle_event
        idle_event.set()

    def connect(self, *args, **kwargs):
        connected = True
        return connected

    def disconnect(self):
        connected = False
        return connected

    def play(self):
        state = "play"

    def pause(self):
        state = "pause"

    def search(self, *args):
        search_keys = args[::2]
        search_args = args[1::2]

        key_translations = {'filename': 'file'}

        search_keys = [k if k not in key_translations else key_translations[k] for k in search_keys]
        
        results = []
        for track in sample_tracks:
            if all( [search_val in track[search_key] for (search_key, search_val) in zip(search_keys, search_args)] ):
                results.append(track)
        
        return results
    
    def addid(self, filename):
        for track in sample_tracks:
            if track['file'] == filename:
                added_track = track
                added_track['pos'] = max([x['pos'] for x in self.track_list] + [-1]) + 1
                added_track['id'] = max([x['id'] for x in self.track_list] + [-1]) + 1
                self.track_list.append(added_track)
                break

        self.send_idle()
        #ipc.update_time('playlist', time.time())
        return added_track['pos']

    def moveid(self, track_id, dest_pos):
        # Find the track with track_id in in the track list
        track = None

        for c_track in self.track_list:
            if c_track['id'] == track_id:
                track = c_track

        if track is None:
            return None

        split_pos = dest_pos if track['pos'] < dest_pos else dest_pos
        self.track_list.remove(track)
        first_part = self.track_list[:(split_pos)]
        try:
            first_part.remove(track)
        except ValueError:
            pass
        second_part = self.track_list[(split_pos):]
        try:
            second_part.remove(track)
        except ValueError:
            pass
        self.track_list = first_part + [track] + second_part

        # Update the positions
        for i in range(0, len(self.track_list)):
            self.track_list[i]['pos'] = i

        #ipc.update_time('playlist', time.time())

    def deleteid(self, track_id):
        if len(self.track_list) > 0:
            removal_track = [track for track in self.track_list if track['id']==track_id][0]
            self.track_list.remove(removal_track)
            #ipc.update_time('playlist', time.time())
            self.send_idle()
            return removal_track
        else:
            return None

    def playlistinfo(self):
        return self.track_list

    def status(self):
        return {'bitrate': '160',
         'consume': '1',
         'elapsed': '95.254',
         'playlist': '10',
         'playlistlength': '%d' % len(self.track_list),
         'random': '0',
         'repeat': '0',
         'single': '0',
         'song': '0',
         'songid': '%d' % self.currentsong().get('id', 0),
         'state': 'play',
         'time': '95:278',
         'volume': '100',
         'xfade': '0'}

    def idle(self):
        global idle_event
        idle_event.wait()
        return ["playlist"]

    def currentsong(self):
        if len(self.track_list) > 0:
            return [track for track in self.track_list if track['pos'] == 0][0]
        else:
            return {} # Should be wahtever the default MPD empty response is.

    def clear(self):
        del self.track_list[:]
