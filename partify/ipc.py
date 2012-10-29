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

"""Contains some state that needs to be shared between processes
and some accessor functions to view and modify that state. Makes
heavy use of python's Multiprocessing library."""

import time

from multiprocessing import Lock, Manager

# State that should only be managed from within the functions in this script

last_updated_times = None
manager = None

# Functions to manage the player state shared information
def init_desired_player_state():
    """Initializes the Manager for the ``desired_player_state``
    information."""
    global manager
    global desired_player_state

    if manager is None:
        manager = Manager()
    if desired_player_state is None:
        desired_player_state = manager.dict()

    desired_player_state['state'] = "play"
    desired_player_state['trans_fn'] = "play"

def update_desired_player_state(state, transition_fn):
    """Updates the state that we want the player to be in for the next
    call to the consistency function.

    :param state: The state we want the player to be in
    :type state: string
    :param transition_fn: The function to call to get the player into the desired state
    :type transition_fn: callable
    """
    global manager
    global desired_player_state

    desired_player_state['state'] = state
    desired_player_state['trans_fn'] = transition_fn

def get_desired_player_state():
    """Tells us what state we want the player to be in.

    :returns: A tuple containing the desired state and the function to get there.
    :rtype: tuple (string, callable)
    """

    global manager
    global desired_player_state

    return desired_player_state['state'], desired_player_state['trans_fn']

desired_player_state = None

# Functions to manage the update times shared information
def init_times():
    """Initializes the Manager for the ``last_updated_times`` dict
    which tracks the times that certain events happen, such as
    playlist updates."""
    global manager
    global last_updated_times
    if manager is None:
        manager = Manager()
    if last_updated_times is None:
        last_updated_times = manager.dict()
    last_updated_times["playlist"] = time.time()

def update_time(key, time):
    """Updates ``last_updated_times`` with a key and the value for that
    key.

    :param key: The key in ``last_updated_times`` to update
    :type key: string
    :param time: The time to store for ``key``
    :type time: float"""
    global manager
    global last_updated_times
    last_updated_times[key] = time

def get_time(key):
    """Gets the value for ``key`` in ``last_updated_times``.

    :param key: The key in ``last_updated_times`` to get
    :type key: string
    :returns: The time corresponding to ``key`` in ``last_updated_times``
    :rtype: float
    """
    global manager
    global last_updated_times
    if key not in last_updated_times:
        last_updated_times[key] = 0
    return last_updated_times[key]

mpd_lock = None

# Functions to manage the locking mechanism between requests and playlist update callbacks
def init_mpd_lock():
    """Initializes the Lock that is used to prevent badness in accessing MPD."""
    global mpd_lock
    if mpd_lock is None:
        mpd_lock = Lock()

def get_mpd_lock():
    """Acquires the lock needed to access MPD."""
    global mpd_lock
    mpd_lock.acquire()

def release_mpd_lock():
    """Releases the MPD lock."""
    global mpd_lock
    mpd_lock.release()

