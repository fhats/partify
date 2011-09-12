$ = jQuery

$ ->
    initPlayer()

initPlayer = () -> 
    initPlayerVisuals()
    initPlayerUpdating()

initPlayerVisuals = () ->
    $("#player_progress").progressbar value: 0
    $("#tabs").tabs()

initPlayerUpdating = () ->
    # Set up push events
    _initPlayerPushUpdates()

    # Set up intermittent polling for synchronization
    _initPlayerSynchroPolling 5000

_initPlayerPushUpdates = () ->
    # Use WebWorkers here to get around the fact that most modern browsers 
    # hang using SSEs...
    worker = new Worker('static/js/partify/workers/player_event.js')

    worker.addEventListener 'message', (e) =>
        console.log e.data
    , false

    worker.postMessage 'Hello world!'

_initPlayerSynchroPolling = (poll_frequency) ->
    # poll_frequnecy is in ms
    setInterval () => 
        _synchroPollAndSchedule()
    , poll_frequency

_synchroPollAndSchedule = () ->
    $.ajax(
        url: 'player/status/poll'
        method: 'GET'
        success: (data) =>
            updatePlayerInfo data
    )

updatePlayerInfo = (data) -> 
    _updatePlayerInfo 'track', data.title
    _updatePlayerInfo 'artist', data.artist
    _updatePlayerInfo 'album', data.album
    _updatePlayerProgress Math.round( (data.elapsed / data.time)*100 )

_updatePlayerInfo = (info_key, data) -> 
    info_span = $("#player_info_" + info_key).first()
    info_span.text data

_updatePlayerProgress = (progress) ->
    $("#player_progress").progressbar value: progress
