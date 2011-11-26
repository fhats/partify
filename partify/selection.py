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

import itertools
from itertools import izip_longest

from sqlalchemy import and_

from partify.models import PlayQueueEntry, User, Vote

def get_selection_scheme(scheme):
    return selection_schemes[scheme]

def get_users_next_pqe_entry_after_playback_priority(user_id, playback_priority):
    return PlayQueueEntry.query.filter(and_(PlayQueueEntry.user_id == user_id, PlayQueueEntry.playback_priority > playback_priority)).order_by(PlayQueueEntry.user_priority.asc()).first()

def _match_tracks_with_users(mpd, db_tracks, user_list):
    for (track,user) in zip(db_tracks, user_list):
        # Check to make sure the next track's user matches the user being looked at.
        # If it doesn't, reorder to move that user's track to this position
        # Otherwise, continue onward 'cause everything cool!
        if track.user == user:
            # all that needs to happen in this situation is to check to see if the current track should be the user's next (i.e. that play order is respected)
            # if it's not, then shuffle some things around until it is.
            if PlayQueueEntry.query.filter(and_(PlayQueueEntry.user == track.user, PlayQueueEntry.user_priority < track.user_priority, PlayQueueEntry.playback_priority > track.playback_priority)).count() > 0:
                # Get the track after the current playback priority with the minimum user_priority and make that the current track
                new_next_track = get_users_next_pqe_entry_after_playback_priority(track.user_id, track.playback_priority)
                if new_next_track is not None:
                    mpd.moveid(new_next_track.mpd_id, track.playback_priority)
                break
            else:
                # Everything's cool!
                pass
        else:
            # Uh-oh!
            # Something isn't round robin about this.
            # To resolve this, push the rest of the tracks back and move the user's lowest pqe after the current playback_priority to the current position.
            new_next_track = get_users_next_pqe_entry_after_playback_priority(user.id, track.playback_priority)
            if new_next_track is not None:
                mpd.moveid(new_next_track.mpd_id, track.playback_priority)
            break

def round_robin(mpd, db_tracks):
    # First, grab a list of all users that currently have PlayQueueEntrys (we can interpret this as active users)
    users = set([pqe.user for pqe in PlayQueueEntry.query.all()])
    unique_users = users = sorted(users, key=lambda d: getattr(d, 'username', 'anonymous'))
    # Turn the sorted user list into a cycle for repeated iteration
    users = itertools.cycle(users)
    current_user = (PlayQueueEntry.query.order_by(PlayQueueEntry.playback_priority.asc()).first()).user

    # Advance the user list to the current user
    users = itertools.dropwhile(lambda x: x != current_user, users)

    user_list = []
    user_counts = dict( (user, PlayQueueEntry.query.filter(PlayQueueEntry.user == user).count()) for user in unique_users )

    # generate a list of users to zip against the track list
    for user in users:
        if all( [user_count == 0 for user_count in user_counts.itervalues()] ):
            break
        
        if user_counts[user] > 0:
            user_counts[user] -= 1
            user_list.append(user)

    _match_tracks_with_users(mpd, db_tracks, user_list)

def first_come_first_served(mpd, db_tracks):
    user_list = [pqe.user for pqe in PlayQueueEntry.query.order_by(PlayQueueEntry.time_added.asc()).all()]

    _match_tracks_with_users(mpd, db_tracks, user_list)

def first_come_first_served_with_voting(mpd, db_tracks):
    # TODO: replace this with a nice SQLAlchemy query
    def sort_fn(x,y):
        votes_x = sum([v.direction for v in Vote.query.filter(Vote.pqe_id==x.id).all()])
        votes_y = sum([v.direction for v in Vote.query.filter(Vote.pqe_id==y.id).all()])
        if votes_x == votes_y:
            if x.time_added < y.time_added:
                return 1
            elif x.time_added == y.time_added:
                return 0
            else:
                return -1    
        else:
            return votes_x - votes_y

    sorted_tracks = sorted(db_tracks[1:], cmp=sort_fn, reverse=True)

    for (sorted_track, db_track) in zip(sorted_tracks, db_tracks[1:]):
        if sorted_track.mpd_id != db_track.mpd_id:
            mpd.moveid(sorted_track.mpd_id, db_track.playback_priority)
            break


selection_schemes = {
    'ROUND_ROBIN': round_robin,
    'FCFS': first_come_first_served,
    'FCFS_VOTE': first_come_first_served_with_voting
}

needs_voting = {
    'ROUND_ROBIN': False,
    'FCFS': False,
    'FCFS_VOTE': True
}
