from multiprocessing import Process

from partify import app
from partify.models import Track, PlayQueueEntry, User

now_playing_info = {}

def scrobble_for_user(user_id, track_id):
    """Takes a user id and track id and scrobble the track represented by track_id for user_id, provided they have given us Last.fm credentials."""
    track = Track.query.get(track_id)
    user = User.query.get(user_id)

    app.logger.info("Scrobbling track %r for user %r" % (track, user))
    
    pass

def queue_user_scrobble(user_id, track_id):
    """Queues a scrobble for a user. Does not immediately submit the scrobble, but instead queues the scrobble and ensures that a scrobble request does not get made twice."""
    track = Track.query.get(track_id)
    user = User.query.get(user_id)

    app.logger.info("Queueing a scrobble of track %r for user %r" % (track, user))

    pass

def process_scrobbles():
    """Steps through the queue of scrobble to process and uses a fire-and-forget mechanism to submit the scrobbles."""

    app.logger.debug("Processing the queue of scrobbles...")
    pass

def now_playing_for_user(user_id, track_id):
    track = Track.query.get(track_id)
    user = User.query.get(user_id)

    app.logger.info("Now playing track %r for user %r" % (track, user))
    pass

def queue_now_playing_for_user(user_id, pqe):
    if user_id not in now_playing_info or now_playing_info[user_id] != pqe.id:
        now_playing_info[user_id] = pqe.id
        # launch a background process to try to update Last.fm information. This fire-and-forget style is fine because if the attempt fails Last.fm says we *should not* retry it.
        p = Process(target=now_playing_for_user, args=(user_id, pqe.track_id))
        p.start()