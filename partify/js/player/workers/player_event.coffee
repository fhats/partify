self.addEventListener 'message', (e) =>
	# Do this outside of here... if !!window.EventSource
    source = new EventSource '/player/status/idle'
    source.addEventListener 'player', (e) =>
        data = JSON.parse e.data
        self.postMessage data
    , false
, false