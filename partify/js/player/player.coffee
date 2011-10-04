$ = jQuery

$ ->
    # Initial setup of the Player object and namespacing within front-end
    window.Partify = window.Partify || {}
    window.Partify.Player = new Player()
    window.Partify.Player.init()
    window.Partify.Queues = window.Partify.Queues || {}
    window.Partify.Queues.GlobalQueue = window.Partify.Queues.GlobalQueue || {}

class Player
    # Class responsible for the functions of the "player", which displays information about the currently playing track
    constructor: () ->
        @info =
            artist: ''
            title: ''
            album: ''
            elapsed: 0
            time: 100
            date: 1970
            volume: 0
            state: 'pause'
            file: ''
            last_global_playlist_update: 0
        @config =
            up_next_items = 3

    init: () -> 
        this.initPlayerVisuals()
        this.initPlayerUpdating()
        @info.last_global_playlist_update = (new Date()).getMilliseconds()

    initPlayerVisuals: () ->
        $("#player_progress").progressbar value: 0
        # This is not really related to the player and should move elsewhere eventually.
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
        # Initializes and is responsible for running polling updates with the server
        this._synchroPoll()

        # poll_frequnecy is in ms
        setInterval () => 
            this._synchroPoll()
        , poll_frequency

    _synchroPoll: () ->
        # Performs the polling updates with the server
        $.ajax(
            url: 'player/status/poll'
            method: 'GET'
            data: 
                current: @info.last_global_playlist_update
            success: (data) =>
                # Compensate for any appreciable lag between the server's response time and the time of the reception of the data
                # (network lag)
                d = new Date()
                current_time = d.getTime() / 1000.0
                lag = current_time - data.response_time
                lag = 0 if lag < 0
                data.elapsed = parseFloat(data.elapsed) + parseFloat(lag)

                this.updatePlayerInfo data

                if data.global_queue
                    window.Partify.Queues.GlobalQueue.update(data.global_queue)
                if data.user_queue
                    window.Partify.Queues.UserQueue.update data.user_queue
        )

    _initPlayerLocalUpdate: () ->
        # Sets up the timer that updates the player's progressbar every second
        setInterval () =>
            this._playerLocalUpdate()
        , 1000
            
    _playerLocalUpdate: () ->
        # Updates the player to stay in sync with the Mopidy server without actually polling it.
        if @info.state == 'play'
            @info.elapsed = if Math.round(@info.elapsed) < @info.time then @info.elapsed + 1 else @info.elapsed
            this.updatePlayerProgress()
            if @info.elapsed >= @info.time
                this._synchroPoll()
                window.Partify.Queues.UserQueue.loadPlayQueue()

    updatePlayerInfo: (data) -> 
        # Takes an array of data items and populates the appropriate HTML elements
        info = for key, value of @info
            data[key] or= @info[key] # Fills in data with information from info in case that key does not exist in data. Prevents nasty undefineds everywhere
            @info[key] = data[key]
            # Special cases!
            if key == 'date'
                d = new Date(data[key])
                @info[key] = d.getFullYear()
        this._updatePlayerTextFromInfo text for text in ['artist', 'title', 'album', 'date']
        this.updatePlayerProgress()

    _updatePlayerTextFromInfo: (info_key) -> 
        # Responsible for updating player text from info in the player class
        this._updatePlayerText info_key, @info[info_key]

    _updatePlayerText: (info_key, data) ->
        # Responsible for updating text associated with the player
        info_span = $("#player_info_" + info_key).first()
        info_span.text data

    updatePlayerProgress: () ->
        # Update the actual progressbar element
        progress = Math.round( (@info.elapsed / @info.time) * 100 )
        $("#player_progress").progressbar value: progress
        this._updatePlayerText 'elapsed', secondsToTimeString @info['elapsed']
        this._updatePlayerText 'time', secondsToTimeString @info['time']

secondsToTimeString = (seconds) ->
    # Converts a number of seconds to a string representing a human-readable time (eg. MM:SS)
    seconds = Math.round(seconds)
    minutes = Math.floor( seconds / 60 )
    seconds = (seconds % 60)
    time_s = "" + minutes + ":"
    # zero-padding
    time_s += if seconds < 10 then '0' else ''
    time_s += seconds
    time_s

Array::remove = (e) -> @[t..t] = [] if (t = @indexOf(e)) > -1
