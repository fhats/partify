"""Copyright 2011 Fred Hatfull

This file is part of Partify.

Partify is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Partify is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Partify.  If not, see <http://www.gnu.org/licenses/>."""

import time
from multiprocessing import Manager, Queue

from partify import ipc
from testing.data.sample_tracks import sample_tracks
# Be careful with this...
try:
    idle_event_queue
except NameError:
    idle_event_queue = Queue()

try:
    manager
except NameError:
    manager = Manager()

try:
    track_list
except NameError:
    track_list = manager.list()


class MockMPDClient(object):
    """A mock MPD client which does not actually connect to an MPD server but acts like it does."""

    connected = False

    def connect(self, *args, **kwargs):
        connected = True
        return connected

    def disconnect(self):
        connected = False
        return connected

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
        global track_list
        for track in sample_tracks:
            if track['file'] == filename:
                added_track = track
                added_track['pos'] = max([x['pos'] for x in track_list] + [-1]) + 1
                added_track['id'] = max([x['id'] for x in track_list] + [-1]) + 1
                track_list.append(added_track)
                break

        ipc.update_time('playlist', time.time())
        return added_track['pos']

    def moveid(self, track_id, dest_pos):
        ipc.update_time('playlist', time.time())

    def deleteid(self, track_id):
        global track_list
        removal_track = [track for track in track_list if track['id']==track_id][0]
        track_list.remove(removal_track)
        ipc.update_time('playlist', time.time())
        return removal_track

    def playlistinfo(self):
        global track_list
        return track_list

    def status(self):
        global track_list
        return {'bitrate': '160',
         'consume': '1',
         'elapsed': '95.254',
         'playlist': '10',
         'playlistlength': '%d' % len(track_list),
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
        while True:
            a = 1+1

    def currentsong(self):
        global track_list
        if len(track_list) > 0:
            return [track for track in track_list if track['pos'] == 0][0]
        else:
            return {} # Should be wahtever the default MPD empty response is.
