from flask import jsonify, request, session, url_for

from partify import app
from partify.decorators import with_mpd

@app.route('/track/search', methods=['GET'])
@with_mpd
def track_search(mpd):
    """Performs a search on the MPD server for tracks matching the specified criteria (as arguments in the URL i.e. HTTP GETs)."""
    mpd_search_terms = []
    for term in ('artist', 'title', 'album'):
        if term in request.args:
            mpd_search_terms.append(term)
            mpd_search_terms.append(request.args[term])
      
    response = {}
          
    if len(mpd_search_terms) > 0:
        results = mpd.search(*mpd_search_terms)
        response['status'] = 'ok'
        response['results'] = results
    else:
        response['status'] = 'error'
        response['message'] = 'No search criteria specified!'
    return jsonify(response)