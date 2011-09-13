$ = jQuery

$ ->
    window.Partify = {}
    window.Partify.Player = new Player()
    window.Partify.Player.init()

class Player
    constructor: () ->
        @info =
            artist: ''
            title: ''
            album: ''
            elapsed: 0
            time: 100
            year: 1970
            volume: 0
            state: 'pause'
            file: ''

    init: () -> 
        this.initPlayerVisuals()
        this.initPlayerUpdating()

    initPlayerVisuals: () ->
        $("#player_progress").progressbar value: 0
        $("#tabs").tabs()

    initPlayerUpdating: () ->
        # Set up push events
        #_initPlayerPushUpdates()

        # Set up intermittent polling for synchronization
        this._initPlayerSynchroPolling 3000

        # Update the progress counter without needing to hit the server every time
        this._initPlayerLocalUpdate()

    _initPlayerPushUpdates: () ->
        # Use WebWorkers here to get around the fact that most modern browsers 
        # hang using SSEs...
        worker = new Worker('static/js/partify/workers/player_event.js')

        worker.addEventListener 'message', (e) =>
            console.log e.data
        , false

        worker.postMessage 'Start checking push'

    _initPlayerSynchroPolling: (poll_frequency) ->
        this._synchroPollAndSchedule()

        # poll_frequnecy is in ms
        setInterval () => 
            this._synchroPollAndSchedule()
        , poll_frequency

    _synchroPollAndSchedule: () ->
        $.ajax(
            url: 'player/status/poll'
            method: 'GET'
            success: (data) =>
                # Compensate for any appreciable lag between the server's response time and the time of the reception of the data
                # (network lag)
                d = new Date()
                current_time = d.getTime() / 1000.0
                lag = current_time - data.response_time
                lag = 0 if lag < 0
                data.elapsed = parseFloat(data.elapsed) + parseFloat(lag)

                this.updatePlayerInfo data
        )

    _initPlayerLocalUpdate: () ->
        setInterval () =>
            this._playerLocalUpdate()
        , 1000
            
    _playerLocalUpdate: () ->
        @info.elapsed = if Math.round(@info.elapsed) < @info.time then @info.elapsed + 1 else @info.elapsed
        this.updatePlayerProgress()

    updatePlayerInfo: (data) -> 
        info = for key, value of @info
            @info[key] = data[key]
        this._updatePlayerTextFromInfo text for text in ['artist', 'title', 'album', 'year']
        this.updatePlayerProgress()

    _updatePlayerTextFromInfo: (info_key) -> 
        this._updatePlayerText info_key, @info[info_key]

    _updatePlayerText: (info_key, data) ->
        info_span = $("#player_info_" + info_key).first()
        info_span.text data

    updatePlayerProgress: () ->
        progress = Math.round( (@info.elapsed / @info.time) * 100 )
        $("#player_progress").progressbar value: progress
        this._updatePlayerText 'elapsed', secondsToTimeString @info['elapsed']
        this._updatePlayerText 'time', secondsToTimeString @info['time']

secondsToTimeString = (seconds) ->
    seconds = Math.round(seconds)
    minutes = Math.floor( seconds / 60 )
    seconds = (seconds % 60)
    time_s = "" + minutes + ":"
    time_s += if seconds < 10 then '0' else ''
    time_s += seconds
    time_s

